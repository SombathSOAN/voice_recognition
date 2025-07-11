import speech_recognition
import webbrowser
from deep_translator import GoogleTranslator
import urllib.parse

def recognize_and_search():
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()

    print("Listening for your search query (Khmer)...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech in Khmer
        khmer_query = recognizer.recognize_google(audio, language="km-KH")
        print(f"You said (Khmer): {khmer_query}")

        # Translate Khmer query to English using Deep Translator
        english_query = GoogleTranslator(source='km', target='en').translate(khmer_query)
        print(f"Translated to English: {english_query}")

        # URL-encode the translated query
        encoded_query = urllib.parse.quote(english_query)

        # Open browser to your search page with query
        base_search_url = "https://e-catalog.dahoughengenterprise.com/search?q="
        webbrowser.open(base_search_url + encoded_query)

    except speech_recognition.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except speech_recognition.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    recognize_and_search()

# You need to install the deep-translator package:
# pip install deep-translator
