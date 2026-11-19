
import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.smallest.ai/waves/v1/tts"
API_KEY = os.getenv("SMALLEST_API_KEY")

base_payload = {
    "text": "Testing request and session ID validation.",
    "voice_id": "kaitlyn",
    "model": "lightning_v3.1_pro",
    "sample_rate": 24000,
    "speed": 1,
    "output_format": "mp3"
}


def run_test(name, extra_fields):
    payload = {**base_payload, **extra_fields}

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            URL,
            json=payload,
            headers=headers,
            timeout=60
        )

        print("\nTEST:", name)
        print("Status:", response.status_code)
        print("Latency:", round(response.elapsed.total_seconds(), 4))
        print("Server Request ID:",
              response.headers.get("X-Request-Id"))
        print("External Request ID:",
              response.headers.get("X-External-Request-Id"))
        print("External Session ID:",
              response.headers.get("X-External-Session-Id"))
        print("Content-Type:",
              response.headers.get("Content-Type"))

        if "application/json" in response.headers.get(
            "Content-Type", ""
        ):
            print("Body:", response.json())

    except requests.RequestException as error:
        print("Error:", error)


# Control: valid IDs
run_test("Valid IDs", {
    "session_id": "qa_session_001",
    "request_id": "qa_request_001"
})

# Invalid session ID: spaces
run_test("Invalid session ID", {
    "session_id": "bad session id"
})

# Invalid request ID: spaces
run_test("Invalid request ID with spaces", {
    "request_id": "bad request id"
})

# Invalid request ID: 129 characters
run_test("129 character request ID", {
    "request_id": "a" * 129
})
