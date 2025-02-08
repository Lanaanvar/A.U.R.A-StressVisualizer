from fastapi import APIRouter
from pydantic import BaseModel
# from ..services import sentiment_analysis, emodetect  # Changed imports to relative
# from ..services.response import get_response  # Import generate_response
# from ..services.preprocessing import preprocess_text  # Import preprocess_text
from ..services import sentiment_analysis, emodetect
from ..services.response import get_response
from ..services.preprocessing import preprocess_text
import logging

router = APIRouter()

class AnalyzeRequest(BaseModel):
    input_text: str

@router.post("/analyze")
async def analyze_input(request: AnalyzeRequest):
    try:
        logging.info("Starting text preprocessing")
        cleaned_text = preprocess_text(request.input_text)  # Use preprocess_text from preprocessing module
        logging.info("Text preprocessing completed")

        logging.info("Starting sentiment analysis")
        sentiment, sentiment_score = sentiment_analysis.analyze(cleaned_text)
        logging.info("Sentiment analysis completed")

        logging.info("Starting emotion detection")
        emotion_analyzer = emodetect.EmotionAnalyzer()  # Create an instance of EmotionAnalyzer
        emotions = emotion_analyzer.detect(cleaned_text)  # Call the detect method on the instance
        logging.info("Emotion detection completed")

        logging.info("Starting response generation")
        tips = get_response(emotions, request.input_text)  # Fix the call to generate_response
        logging.info("Response generation completed")

        return {
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "emotions": emotions,
            "tips": tips,
            # "stress_level": stress_level
        }
    except Exception as e:
        logging.error(f"Error during analysis: {e}", exc_info=True)  # Log the full stack trace
        raise e