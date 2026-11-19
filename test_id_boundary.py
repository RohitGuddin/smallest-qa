
import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.smallest.ai/waves/v1/tts"
API_KEY = os.getenv("SMALLEST_API_KEY")

base_payload = {
    "text": "Testing ID length validation.",
    "voice_id": "kaitlyn",
    "model": "lightning_v3.1_pro",
    "sample_rate": 24000,
    "speed": 1,
    "output_format": "mp3"
}

tests = [
    ("129-character request ID", {
        "request_id": "a" * 129
    }),
    ("129-character session ID", {
        "session_id": "a" * 129
    })
]

for name, extra in tests:
    print("\nTEST:", name)

    try:
        response = requests.post(
            URL,
            json={**base_payload, **extra},
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=(5, 20)
        )

        print("Status:", response.status_code)
        print("Latency:", round(response.elapsed.total_seconds(), 3))
        print("Server Request ID:",
              response.headers.get("X-Request-Id"))
        print("External Request ID:",
              response.headers.get("X-External-Request-Id"))
        print("External Session ID:",
              response.headers.get("X-External-Session-Id"))

        if "application/json" in response.headers.get(
            "Content-Type", ""
        ):
            print("Body:", response.json())

    except requests.Timeout:
        print("TIMEOUT: No response within configured timeout")

    except requests.RequestException as error:
        print("Request error:", error)
