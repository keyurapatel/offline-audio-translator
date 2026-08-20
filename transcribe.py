import wave
import json
import whisper
from vosk import Model, KaldiRecognizer

# Load whisper tiny model once
whisper_model = whisper.load_model("tiny")

VOSK_MODELS = {
    "en": "models/en",
    "hi": "models/hi",
    "gu": "models/gu"
}

LANG_MAP = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati"
}


def detect_language(audio_path):
    result = whisper_model.transcribe(audio_path, task="transcribe")
    return result["language"]


def transcribe(audio_path):
    # 1️⃣ Detect language using Whisper
    detected_lang = detect_language(audio_path)

    # fallback to English if not supported
    if detected_lang not in VOSK_MODELS:
        detected_lang = "en"

    model_path = VOSK_MODELS[detected_lang]
    model = Model(model_path)

    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if result.get("text"):
                results.append(result["text"])

    final = json.loads(rec.FinalResult())
    if final.get("text"):
        results.append(final["text"])

    clean_text = " ".join(dict.fromkeys(results))

    return clean_text.strip(), LANG_MAP[detected_lang]
