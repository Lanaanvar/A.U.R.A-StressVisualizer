from fastapi import FastAPI
from app.api.routes import router  # Adjust the import path as necessary
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(router, prefix="/api")