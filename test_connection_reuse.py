
import os, json, asyncio, time
import websockets
from dotenv import load_dotenv

load_dotenv()

URL = "wss://api.smallest.ai/waves/v1/tts/live"
KEY = os.getenv("SMALLEST_API_KEY")

async def main():
    try:
        async with websockets.connect(
            URL,
            additional_headers={"Authorization": f"Bearer {KEY}"},
            open_timeout=15,
            close_timeout=5
        ) as ws:

            for number in (1, 2):
                payload = {
                    "text": "Hello. This is a test of real time speech generation.",
                    "voice_id": "meher",
                    "model": "lightning_v3.1_pro",
                    "sample_rate": 24000
                }

                print(f"\nSending request {number}", flush=True)
                await ws.send(json.dumps(payload))

                chunks = 0
                start = time.perf_counter()

                while True:
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=15)
                    except asyncio.TimeoutError:
                        print(f"TIMEOUT on request {number}", flush=True)
                        return

                    msg = json.loads(raw)
                    status = msg.get("status")

                    if status == "chunk":
                        chunks += 1
                    elif status == "complete":
                        print(
                            f"Request {number} completed; "
                            f"chunks={chunks}; "
                            f"elapsed={time.perf_counter()-start:.3f}s",
                            flush=True
                        )
                        break
                    else:
                        print("Unexpected frame:", msg, flush=True)

            print("\nBoth requests completed.", flush=True)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e.code}, {e.reason}", flush=True)
    except Exception as e:
        print("ERROR:", type(e).__name__, str(e), flush=True)

asyncio.run(main())
