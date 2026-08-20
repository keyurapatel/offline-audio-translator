from textblob import TextBlob
import nltk
nltk.download('punkt')

def sentence_wise_sentiment(text):
    sentences = nltk.sent_tokenize(text)  # split into sentences
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
