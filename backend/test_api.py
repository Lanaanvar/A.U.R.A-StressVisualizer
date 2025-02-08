import requests
import json

url = "http://127.0.0.1:8000/api/analyze"
data = {
    "input_text": "I can feel the heat building inside, like a storm ready to erupt. My thoughts are sharp, every word I want to say cutting through the air like a blade. It’s a burning frustration, a tightness in my chest, my fists clenched in a desperate attempt to hold it in. Every little thing feels like it’s pushing me further, digging deeper into this feeling of being unheard, disrespected. It’s like there’s no room to breathe, no way to escape the tension that’s just waiting to explode. Why does it always feel like nothing changes, like the anger never really goes away?"
}

response = requests.post(url, json=data)

print(f"Status Code: {response.status_code}")

try:
    response_json = response.json()
    print("Response JSON:")
    print(json.dumps(response_json, indent=4))
except requests.exceptions.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
