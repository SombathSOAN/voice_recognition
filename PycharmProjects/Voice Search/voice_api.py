from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from io import BytesIO
from pydub import AudioSegment
import os

# Load environment
load_dotenv()

class Settings(BaseSettings):
    google_project: str = os.getenv("GOOGLE_CLOUD_PROJECT")
    cors_origins: list[str] = os.getenv("CORS_ALLOW_ORIGINS", "").split(",")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))
    log_level: str = os.getenv("LOG_LEVEL", "info")
    base_search_url: str = os.getenv("BASE_SEARCH_URL", "https://e-catalog.dahoughengenterprise.com/search?q=")
    source_lang: str = os.getenv("SOURCE_LANG", "km-KH")
    target_lang: str = os.getenv("TARGET_LANG", "en")

settings = Settings()

import speech_recognition
from google.cloud import translate_v2 as translate
import urllib.parse
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["POST"],
    allow_headers=["*"],
)

recognizer = speech_recognition.Recognizer()
translator_client = translate.Client()

@app.post("/voice-search/")
async def voice_search(audio: UploadFile = File(...)):
    try:
        data = await audio.read()
        # Convert incoming audio (wav, flac, m4a, mp3, etc.) to 16-bit mono WAV
        audio_ext = audio.filename.split('.')[-1].lower()
        wav_audio = AudioSegment.from_file(BytesIO(data), format=audio_ext)
        wav_io = BytesIO()
        wav_audio.export(wav_io, format='wav', parameters=['-ar', '16000', '-ac', '1'])
        wav_io.seek(0)

        with speech_recognition.AudioFile(wav_io) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
    except Exception as e:
        raise HTTPException(400, f"Failed to process audio file: {e}")

    try:
        khmer = recognizer.recognize_google(audio_data, language=settings.source_lang)
    except speech_recognition.UnknownValueError:
        raise HTTPException(422, "Could not understand the audio")
    except Exception as e:
        raise HTTPException(500, f"Recognition error: {e}")

    try:
        result = translator_client.translate(
            khmer,
            source_language=settings.source_lang.split("-")[0],
            target_language=settings.target_lang
        )
        english = result["translatedText"]
    except Exception as e:
        raise HTTPException(500, f"Translation error: {e}")

    search_url = settings.base_search_url + urllib.parse.quote(english)
    return {"khmer_query": khmer, "english_query": english, "search_url": search_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "voice_api:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level
    )