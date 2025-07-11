Below is a suggested **README.md** for your **Voice Recognition** project. You can create a new file named `README.md` at the root of your repo and paste this in.

````markdown
# Voice Recognition Search

> 🎙️ **Speak Khmer. Search English.**  
> A simple Python tool that listens to your Khmer voice, translates it to English via Google Cloud Translation, and opens your e-catalog search in a browser.

---

## 🚀 Features

- **Khmer speech recognition** using `SpeechRecognition` + `PyAudio`
- **High-quality translation** via Google Cloud Translation API (Application Default Credentials)
- **Auto URL-encoding** of translated queries  
- **Browser integration** to instantly launch your e-catalog search

---

## 🛠️ Prerequisites

- **macOS** (or Linux)  
- **Python 3.9+**  
- [Homebrew](https://brew.sh/) (for installing PortAudio & gcloud CLI)  
- A Google Cloud project with **Translation API** enabled  

---

## ⚙️ Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/SombathSOAN/voice_recognition.git
   cd voice_recognition
````

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate     # macOS/Linux
   ```

3. **Install audio & speech libs**

   ```bash
   brew install portaudio
   pip install SpeechRecognition pyaudio
   ```

4. **Install Google Cloud CLI**

   ```bash
   brew install --cask google-cloud-sdk
   gcloud init
   ```

5. **Install Python dependencies**

   ```bash
   pip install google-cloud-translate
   ```

---

## 🔑 Authentication (ADC)

We use **Application Default Credentials** to authenticate without JSON key files.

1. **Login your user account**

   ```bash
   gcloud auth login
   ```

2. **Bootstrap ADC credentials**

   ```bash
   gcloud auth application-default login
   ```

3. **Set your active & quota project**

   ```bash
   gcloud config set project e-catalog-2d935
   gcloud auth application-default set-quota-project e-catalog-2d935
   ```

4. **Enable the Translation API**

   ```bash
   gcloud services enable translate.googleapis.com
   ```

---

## ▶️ Usage

With your `.venv` active and all prerequisites met:

```bash
python voice_recoginitor.py
```

* Speak naturally in **Khmer**.
* The tool will print:

  * Your raw Khmer text
  * Its English translation
  * Then pop open a browser pointing to:

```
https://e-catalog.dahoughengenterprise.com/search?q=<URL-encoded English text>
```

---

## 📝 Troubleshooting

* **“ModuleNotFoundError”**
  Make sure you installed `SpeechRecognition`, `pyaudio`, and `google-cloud-translate` *inside* `.venv`.
* **Translation errors or empty output**
  Verify your ADC setup (`gcloud auth application-default login`) and that your project has the Translation API enabled.

---

## 🔭 Next Steps

* Add **text-to-speech** feedback (e.g. `pyttsx3`) for confirmations.
* Build a minimal **GUI** or **daemon** for continuous voice-search service.
* Integrate with other back-end endpoints (e.g. product filters, voice commands).

---

## 📄 License

This project is released under the **MIT License**.
Feel free to fork, tweak, and unleash your own voice-powered adventures!

---

> “Speak your mind, one word at a time.”
> — Sombath Sona 😉

```

Feel free to adjust any section to match your repo’s branch names or project ID. Let me know if you’d like any tweaks or extra badges (CI, license, etc.).
::contentReference[oaicite:0]{index=0}
```
