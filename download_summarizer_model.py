from transformers import pipeline

print("Downloading model...")
pipeline("summarization", model="facebook/bart-large-cnn")
print("Model downloaded successfully!")
