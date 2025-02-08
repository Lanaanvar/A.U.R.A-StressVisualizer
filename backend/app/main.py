from fastapi import FastAPI
from .response import get_response

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/generate-response")
def generate_response(emotions: dict):
    return {"response": get_response(emotions)}
