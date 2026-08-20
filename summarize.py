from transformers import pipeline

MODEL_PATH = "models/bart-large-cnn"

summarizer = pipeline(
    "summarization",
    model=MODEL_PATH,
    tokenizer=MODEL_PATH
)

def summarize_text(text):
    max_chunk = 1000
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]

    summary = ""
    for chunk in chunks:
        result = summarizer(chunk, max_length=120, min_length=40, do_sample=False)
        summary += result[0]["summary_text"] + " "

    return summary
