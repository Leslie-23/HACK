import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
import os

client = TestClient(app)

# -------------------------------
# 1️⃣ Test Speech-to-Text (STT)
# -------------------------------
def test_speech_to_text():
    """Test sending an audio file for speech-to-text processing."""
    audio_path = "test_audio.wav"  # Provide a valid test audio file
    
    with open(audio_path, "rb") as file:
        response = client.post("/stt/", files={"audio_file": file})

    assert response.status_code == 200
    assert "transcribed_text" in response.json()

# -------------------------------
# 2️⃣ Test Text-to-Speech (TTS)
# -------------------------------
def test_text_to_speech():
    """Test text-to-speech conversion."""
    response = client.post("/tts/", json={"text": "Hello, this is a test."})

    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Speech generated"
    assert "file" in response.json()

    # Ensure the file was actually created
    assert os.path.exists("output.mp3")

# -------------------------------
# 3️⃣ Test AI Learning (User Speech Adaptation)
# -------------------------------
def test_learn_user_speech():
    """Test storing user speech learning data."""
    data = {
        "user_id": "test_user",
        "text": "Hello World",
        "confirmed": True
    }

    response = client.post("/learn/", json=data)

    assert response.status_code == 200
    assert response.json()["message"] == "User data stored"

# -------------------------------
# ✅ Run Tests
# -------------------------------
if __name__ == "__main__":
    pytest.main()
