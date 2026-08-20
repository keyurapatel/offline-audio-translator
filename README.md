# Offline Audio Translator

Offline audio transcription and translation app using Streamlit, Whisper, Vosk, Transformers, and TextBlob.

## Features

- Upload MP3 or WAV audio files
- Detect audio language automatically
- Transcribe English, Hindi, and Gujarati audio
- Translate text to English, Hindi, and Gujarati
- Generate English summaries
- Show sentence-wise sentiment analysis

## Project Structure

```text
app.py                         Main Streamlit app
download_models.py             Downloads offline translation packages
download_summarizer_model.py   Downloads summarization model
translate.py                   Translation helper
summarize.py                   Summarization helper
transcribe.py                  Transcription helper
sentiment.py                   Sentiment helper
models/                        Local model files, ignored by Git
audio/                         Uploaded/converted audio files, ignored by Git
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install required Python packages:

```powershell
pip install streamlit openai-whisper vosk transformers torch textblob nltk argostranslate
```

Install FFmpeg and make sure `ffmpeg` is available from the terminal.

## Models

This repository does not include large model files. Keep them locally inside `models/`.

Expected Vosk folders:

```text
models/en
models/hi
models/gu
```

Expected summarizer folder:

```text
models/bart-large-cnn
```

Download translation models:

```powershell
python download_models.py
```

Download summarizer model:

```powershell
python download_summarizer_model.py
```

## Run

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Notes

- `.venv`, `models`, `audio`, and `output_text` are ignored by Git.
- If `ModuleNotFoundError` appears, make sure the app is running with `.venv\Scripts\python.exe`.
