
import os
import requests
import uuid
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.smallest.ai/waves/v1/tts"
API_KEY = os.getenv("SMALLEST_API_KEY")

if not API_KEY:
    raise ValueError("API key missing. Check your .env file.")


def test_tts(name, payload, key=API_KEY):
    request_id = f"qa_{uuid.uuid4().hex[:12]}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}" if key else ""
    }

    payload = {
        **payload,
        "request_id": request_id
    }

    try:
        response = requests.post(
            URL,
            json=payload,
            headers=headers,
            timeout=60
        )

        print(f"\n{'=' * 50}")
        print("Test:", name)
        print("Status:", response.status_code)
        print("Latency:", round(response.elapsed.total_seconds(), 4))
        print("Client Request ID:", request_id)
        print("Server Request ID:",
              response.headers.get("X-Request-Id"))
        print("External Request ID:",
              response.headers.get("X-External-Request-Id"))
        print("Content-Type:",
              response.headers.get("Content-Type"))
        print("Response size:", len(response.content))

        if "application/json" in response.headers.get(
            "Content-Type", ""
        ):
            print("Response body:", response.json())
        else:
            print("Binary audio response")

        if response.status_code == 200:
            filename = f"output_{name.replace(' ', '_')}.mp3"
            with open(filename, "wb") as audio:
                audio.write(response.content)
            print("Audio saved:", filename)

        return response

    except requests.RequestException as error:
        print("Request failed:", error)


base_payload = {
    "text": "Hello from Smallest AI QA testing.",
    "voice_id": "kaitlyn",
    "model": "lightning_v3.1_pro",
    "sample_rate": 24000,
    "speed": 1,
    "output_format": "mp3"
}


# T01: Valid request
test_tts("Valid request", base_payload)

# T02: Empty text
test_tts("Empty text", {**base_payload, "text": ""})

# T03: Whitespace-only text
test_tts("Whitespace text", {**base_payload, "text": "     "})

# T04: Maximum text
test_tts("8000 characters",
         {**base_payload, "text": "A" * 8000})

# T05: Exceed maximum
test_tts("8001 characters",
         {**base_payload, "text": "A" * 8001})

# T06: Invalid API key
test_tts("Invalid API key", base_payload, "invalid_key")

# T07: Missing API key
test_tts("Missing API key", base_payload, None)

# T08: Invalid speed
test_tts("Invalid speed",
         {**base_payload, "speed": 3.0})

# T09: Invalid sample rate
test_tts("Invalid sample rate",
         {**base_payload, "sample_rate": 32000})

# T10: Invalid format
test_tts("Invalid format",
         {**base_payload, "output_format": "ogg"})

# T11: Invalid session ID
test_tts("Invalid session ID",
         {**base_payload, "session_id": "bad session id"})

# T12: Invalid request ID
test_tts("Invalid request ID",
         {**base_payload, "request_id": "a" * 129})
