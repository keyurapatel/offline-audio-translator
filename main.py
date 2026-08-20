from convert import convert_to_wav
from transcribe import transcribe
from translate import translate_text
import os

AUDIO = "audio/sample.mp3"
WAV = "audio/sample.wav"

MODELS = {
    "1": "models/en",
    "2": "models/hi",
    "3": "models/gu"
}

print("Starting program...")

if not os.path.exists(AUDIO):
    print("❌ Audio file not found:", AUDIO)
    exit()

print("Converting MP3 to WAV...")
convert_to_wav(AUDIO, WAV)
print("Conversion done.")

print("\nChoose language model:")
print("1. English")
print("2. Hindi")
print("3. Gujarati")

choice = input("Enter number: ")

if choice not in MODELS:
    print("❌ Invalid choice")
    exit()

print("Transcribing audio...")
text = transcribe(WAV, MODELS[choice])

print("Transcription complete.")
print("\nDetected Text:\n")
print(text)


print("Translating...")
translations = translate_text(text)

os.makedirs("output_text", exist_ok=True)

for lang, data in translations.items():
    with open(f"output_text/{lang}.txt", "w", encoding="utf-8") as f:
        f.write(data)

print("✅ Done! Check output_text folder.")
