import re
import spacy
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')
stopwords = set(stopwords.words('english'))

# Preprocessing of input text

def preprocess_text(text):

    text = text.lower()
    text = re.sub(r"http\S+|www\S+|@\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    doc = nlp(text)
    lemmatized_text = [token.lemma_ for token in doc if token.text not in stopwords]

    return " ".join(lemmatized_text)
