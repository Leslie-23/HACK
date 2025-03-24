from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import uvicorn
import speech_recognition as sr
import torchaudio
from gtts import gTTS
import os

app = FastAPI()

# -------------------- Speech-to-Text (STT) --------------------
@app.post("/stt/")
async def speech_to_text(audio_file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file.file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
        return {"transcribed_text": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------- Text-to-Speech (TTS) --------------------
@app.post("/tts/")
async def text_to_speech(text: str):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        return {"message": "Speech generated", "file": "output.mp3"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- AI Learning (User Adaptation) --------------------
class UserSpeechData(BaseModel):
    user_id: str
    text: str
    confirmed: bool  # Whether the user confirmed the word choice

user_database = {}

@app.post("/learn/")
async def learn_user_speech(data: UserSpeechData):
    if data.user_id not in user_database:
        user_database[data.user_id] = []
    user_database[data.user_id].append((data.text, data.confirmed))
    return {"message": "User data stored"}

# -------------------- Run Server --------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
