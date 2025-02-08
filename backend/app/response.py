import os
from dotenv import load_dotenv
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Correctly fetch the API key from environment variable

# Ensure the API key is correctly set
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

def get_response(emotions):
    detected_emotion = max(emotions, key=emotions.get)

    prompt = f"""
    You are a mental health assistant. A user is experiencing {detected_emotion}.
    Provide a short, calming, and actionable stress-relief tip. 
    The advice should vary and can include activities like taking a calming walk, listening to calming music, practicing deep breathing, or any other effective stress-relief techniques. Give varied advices and not just breathing techniques.
    """

    headers = {
        "Content-Type": "application/json"
    }

    params = {
        "key": GEMINI_API_KEY  # Gemini API key is passed as a query parameter
    }

    data = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()

        # Debug: Print full response to inspect structure
        #print(result)

        # Extract response text
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Stay calm and take care of yourself.")

    except Exception as e:
        print(f"Error: {e}")  # Print the error for debugging
        return "Stay calm and take care of yourself."

# Test
emotions = {"sadness": 0.9, "anger": 0.9, "happiness": 0.0, "anxiety": 0.9}
print(get_response(emotions))