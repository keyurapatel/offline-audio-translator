import streamlit as st
import os
import wave
import json
import subprocess
import whisper
from vosk import Model, KaldiRecognizer
from translate import translate_text
from summarize import summarize_text
from textblob import TextBlob
import nltk

nltk.download("punkt")

# ---------------- PATHS ----------------
VOSK_MODELS = {
    "en": "models/en",
    "hi": "models/hi",
    "gu": "models/gu"
}

LANG_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati"
}

LANG_CODES = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "Gujarati": "guj_Gujr"
}

# ---------------- LOAD MODELS ----------------
model_en = Model(VOSK_MODELS["en"])
model_hi = Model(VOSK_MODELS["hi"])
model_gu = Model(VOSK_MODELS["gu"])

whisper_model = whisper.load_model("tiny")

# ---------------- AUDIO CONVERT ----------------
def convert_to_16k_mono(input_audio, output_wav):
    command = [
        "ffmpeg", "-y",
        "-i", input_audio,
        "-ac", "1",
        "-ar", "16000",
        output_wav
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ---------------- SENTIMENT ----------------
def sentence_wise_sentiment(text):
    sentences = nltk.sent_tokenize(text)
    results = []
    for sentence in sentences:
        blob = TextBlob(sentence)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = "Positive 😊"
        elif polarity < 0:
            sentiment = "Negative 😞"
        else:
            sentiment = "Neutral 😐"
        results.append((sentence, sentiment))
    return results

# ---------------- LANGUAGE DETECTION ----------------
def detect_language(audio_path):
    result = whisper_model.transcribe(audio_path, task="transcribe")
    return result["language"]

# ---------------- TRANSCRIBE ----------------
def transcribe_audio(wav_path, detected_lang):
    if detected_lang == "gu":
        model = model_gu
    elif detected_lang == "hi":
        model = model_hi
    else:
        model = model_en

    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            text += res.get("text", "") + " "

    final = json.loads(rec.FinalResult())
    text += final.get("text", "")
    return text.strip()

# ---------------- UI ----------------
st.set_page_config(page_title="Offline Audio Translator", layout="centered")
st.title("🎙️ Offline Audio Translator (Auto Language Detection)")

uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])

if uploaded_file:
    os.makedirs("audio", exist_ok=True)

    input_audio = f"audio/{uploaded_file.name}"
    wav_path = "audio/converted.wav"

    with open(input_audio, "wb") as f:
        f.write(uploaded_file.read())

    st.audio(input_audio)

    if st.button("Process Audio"):

        with st.spinner("Converting audio..."):
            convert_to_16k_mono(input_audio, wav_path)

        with st.spinner("Detecting language..."):
            detected_lang = detect_language(wav_path)

        detected_language_name = LANG_NAMES.get(detected_lang, "English")

        st.subheader("Auto Detected Language")
        st.write(detected_language_name)

        with st.spinner("Transcribing audio..."):
            text = transcribe_audio(wav_path, detected_lang)

        st.subheader("Detected Text")
        st.text_area("Detected Text", text, height=200)

        src_lang = LANG_CODES[detected_language_name]

        # ---------------- TRANSLATION ----------------
        with st.spinner("Translating..."):
            english_text = translate_text(text, src_lang, "eng_Latn")
            hindi_text = translate_text(text, src_lang, "hin_Deva")
            gujarati_text = translate_text(text, src_lang, "guj_Gujr")

        st.subheader("English Translation")
        st.text_area("English", english_text, height=150)

        st.subheader("Hindi Translation")
        st.text_area("Hindi", hindi_text, height=150)

        st.subheader("Gujarati Translation")
        st.text_area("Gujarati", gujarati_text, height=150)

        # ---------------- SUMMARY ----------------
        with st.spinner("Generating Summary..."):
            summary_text = summarize_text(english_text)

        st.subheader("📝 Summary (English)")
        st.text_area("Summary", summary_text, height=120)

        # ---------------- SENTIMENT ----------------
        with st.spinner("Analyzing Sentiment..."):
            sentiment_results = sentence_wise_sentiment(summary_text)

        st.subheader("📊 Sentence-wise Sentiment")
        for sent, senti in sentiment_results:
            st.write(f"{sent} → {senti}")

        st.success("✅ Done!")
