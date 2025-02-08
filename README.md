# StressVisualizer

## Description
StressVisualizer is a project aimed at visualizing and analyzing stress levels using various data processing and machine learning techniques. The backend is implemented using FastAPI.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/StressVisualizer.git
   cd StressVisualizer
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
To run the FastAPI application, use the following command:
```sh
uvicorn main:app --reload
```
This will start the server, and you can access the API at `http://127.0.0.1:8000`.

### Sentiment Analysis Service
The sentiment analysis service uses the Hugging Face `transformers` library and PyTorch to analyze text sentiment. Example usage:
```python
from app.services.sentiment_analysis import analyze

text = "I am feeling great today!"
sentiment, score = analyze(text)
print(f"Sentiment: {sentiment}, Score: {score}")
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
