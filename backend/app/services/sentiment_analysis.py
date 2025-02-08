from transformers import pipeline
import torch

device = 0 if torch.cuda.is_available() else -1

analyser = pipeline('sentiment-analysis', device=device)

#Performing sentiment analysis on the input text

def analyze(text):
    result = analyser(text)
    sentiment = result[0]['label']
    sentiment_score = result[0]['score']

    return sentiment, sentiment_score

