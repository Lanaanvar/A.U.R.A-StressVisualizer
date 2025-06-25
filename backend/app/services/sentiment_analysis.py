from transformers import pipeline
import torch
import logging

device = 0 if torch.cuda.is_available() else -1
logging.info(f"Device set to use {'GPU' if device == 0 else 'CPU'}")

analyser = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

def normalize_score(score):
    return (score - 0.5) * 2

def analyze(text):
    logging.info(f"Analyzing text: {text}")
    result = analyser(text)
    sentiment = result[0]['label']
    sentiment_score = normalize_score(result[0]['score'])
    logging.info(f"Sentiment: {sentiment}, Score: {sentiment_score}")

    return sentiment, sentiment_score

