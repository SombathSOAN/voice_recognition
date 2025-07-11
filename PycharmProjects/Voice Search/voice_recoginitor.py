import speech_recognition
import webbrowser
from google.cloud import translate_v2 as translate
import urllib.parse

import os
from dotenv import load_dotenv

load_dotenv()

BASE_SEARCH_URL = os.getenv("BASE_SEARCH_URL", "https://e-catalog.dahoughengenterprise.com/search?q=")
SOURCE_LANG = os.getenv("SOURCE_LANG", "km-KH")
TARGET_LANG = os.getenv("TARGET_LANG", "en")

def recognize_and_search():
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()
    client = translate.Client()

    print(f"Listening for your search query ({SOURCE_LANG})...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech in Khmer
        khmer_query = recognizer.recognize_google(audio, language=SOURCE_LANG)
        print(f"You said ({SOURCE_LANG}): {khmer_query}")

        # Translate Khmer query to English using Cloud Translation
        result = client.translate(
            khmer_query,
            source_language=SOURCE_LANG.split("-")[0],
            target_language=TARGET_LANG
        )
        english_query = result["translatedText"]
        print(f"Translated to {TARGET_LANG}: {english_query}")

        # URL-encode the translated query
        encoded_query = urllib.parse.quote(english_query)

        # Open browser to your search page with query
        webbrowser.open(BASE_SEARCH_URL + encoded_query)

    except speech_recognition.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except speech_recognition.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    recognize_and_search()

# You need to install the Cloud Translate library:
# pip install google-cloud-translate
