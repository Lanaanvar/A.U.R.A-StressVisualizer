import os
from dotenv import load_dotenv
import requests
from ..services.emodetect import EmotionAnalyzer

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
)


def get_response(text, emotions):
    detected_emotion = max(emotions, key=emotions.get)

    prompt = f"""
    Act as a friend. Your friend is having the following issue: {text} and is experiencing {detected_emotion}.
    As a friend, you want to provide some advice to help them feel better and provide a solution to it.
    The advice, four advices, should vary and mainly include stress-relieving activities or any other effective stress-relief techniques. Give varied advice and present it as a very brief summary.
    """

    headers = {"Content-Type": "application/json"}

    params = {"key": GEMINI_API_KEY}

    data = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}

    try:
        response = requests.post(
            GEMINI_API_URL, headers=headers, params=params, json=data
        )
        response.raise_for_status()
        result = response.json()
        response_text = (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "Stay calm and take care of yourself.")
        )

        # Format the response text
        formatted_response = f"**Detected Emotions:** {', '.join([f'{k}: {v:.2f}' for k, v in emotions.items()])}\n\n**Advice:**\n{response_text}"

        return formatted_response

    except Exception as e:
        print(f"Error: {e}")
        return "Stay calm and take care of yourself."
