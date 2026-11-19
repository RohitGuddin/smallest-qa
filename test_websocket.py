
import os
import json
import time
import asyncio
import websockets
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("SMALLEST_API_KEY")
WS_URL = "wss://api.smallest.ai/waves/v1/tts/live"

async def test_websocket():
    payload = {
        "text": "Hello. This is a test of real time speech generation.",
        "voice_id": "meher",
        "model": "lightning_v3.1_pro",
        "sample_rate": 24000
    }

    print("Started:", datetime.now().astimezone().isoformat())

    try:
        async with websockets.connect(
            WS_URL,
            additional_headers={"Authorization": f"Bearer {API_KEY}"},
            open_timeout=15,
            close_timeout=5
        ) as ws:

            print("Connected successfully")

            await ws.send(json.dumps(payload))
            print("Request sent")

            start = time.perf_counter()
            first_chunk = None
            chunks = 0
            audio_bytes = 0

            while True:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=15)
                except asyncio.TimeoutError:
                    print("TIMEOUT: No frame received for 15 seconds")
                    break

                elapsed = time.perf_counter() - start
                print(f"Frame received after {elapsed:.3f}s")

                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    print("Non-JSON response:", str(raw)[:300])
                    continue

                print("Frame status:", msg.get("status"))
                print("Frame keys:", list(msg.keys()))

                if msg.get("status") == "chunk":
                    if first_chunk is None:
                        first_chunk = elapsed

                    audio = msg.get("data", {}).get("audio", "")
                    chunks += 1
                    import base64
                    decoded = base64.b64decode(audio)
                    audio_bytes += len(decoded)

                elif msg.get("status") == "complete":
                    print("Completion frame received")
                    break

                else:
                    print("Other frame:", msg)

            print("\n--- SUMMARY ---")
            print("Audio chunks:", chunks)
            print("Audio bytes:", audio_bytes)
            print("First chunk latency:", first_chunk)
            print("Connection state:", ws.state)

    except Exception as e:
        print("ERROR:", type(e).__name__, str(e))

if __name__ == "__main__":
    asyncio.run(test_websocket())
