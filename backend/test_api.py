import requests
import json

url = "http://127.0.0.1:8000/api/analyze"
data = {
    "input_text": "I am feeling very stressed and anxious today."
}

response = requests.post(url, json=data)

# Print the response status code and text for debugging
print(f"Status Code: {response.status_code}")

# Attempt to parse the response as JSON
try:
    response_json = response.json()
    print("Response JSON:")
    print(json.dumps(response_json, indent=4))  # Pretty-print the JSON response
except requests.exceptions.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
