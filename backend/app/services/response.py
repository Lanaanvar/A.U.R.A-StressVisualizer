import os
from dotenv import load_dotenv
import requests
import emodetect
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Correctly fetch the API key from environment variable

# Ensure the API key is correctly set
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

def get_response(text, emotions):
    detected_emotion = max(emotions, key=emotions.get)

    prompt = f"""
    Act as a friend. Your friend is having the following issue : {text} and is experiencing {detected_emotion}.
    As a friend, you want to provide some advice to help them feel better and provide a solution to it.
    The advice should vary and mainly include stress-relieving activities or any other effective stress-relief techniques. Give varied advices and present it as a very brief summary"""

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
        response_text = f"Detected emotions: {emotions}"
        #return response_text

        # Debug: Print full response to inspect structure
        #print(response_text)

        # Extract response text
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Stay calm and take care of yourself.")

    except Exception as e:
        print(f"Error: {e}")  # Print the error for debugging
        return "Stay calm and take care of yourself."

# Test
sample_text = """My mind is racing, thoughts ping-ponging from one thing to the next, and I can't seem to focus on just one. I keep imagining every worst-case scenario, even the ones that do not make sense. What if I mess up? What if I forget something important? It is like this tight knot in my stomach that will not loosen, and every little thing feels like it could spiral into something bigger. I am constantly wondering if people are judging me, if I am doing enough, if I am good enough. It's exhausting, and no matter how hard I try, it feels like the worry just keeps piling on."""
analyzer = emodetect.EmotionAnalyzer()    
emotions = analyzer.detect(sample_text)
print(get_response(sample_text, emotions))