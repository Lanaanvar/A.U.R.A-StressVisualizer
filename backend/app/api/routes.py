from fastapi import APIRouter
from pydantic import BaseModel
from ..services import sentiment_analysis, emodetect
from ..services.response import get_response
from ..services.preprocessing import preprocess_text
import logging

router = APIRouter()

# 💡 Load models once during server startup
emotion_analyzer = emodetect.EmotionAnalyzer()

class AnalyzeRequest(BaseModel):
    input_text: str

@router.post("/analyze")
async def analyze_input(request: AnalyzeRequest):
    try:
        logging.info("Starting text preprocessing")
        cleaned_text = preprocess_text(request.input_text)
        logging.info("Text preprocessing completed")

        logging.info("Starting sentiment analysis")
        sentiment, sentiment_score = sentiment_analysis.analyze(cleaned_text)
        logging.info("Sentiment analysis completed")

        logging.info("Starting emotion detection")
        emotions = emotion_analyzer.detect(cleaned_text)
        logging.info("Emotion detection completed")

        logging.info("Starting response generation")
        tips = get_response(request.input_text, emotions)
        logging.info("Response generation completed")

        return {
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "emotions": emotions,
            "tips": tips,
        }
    except Exception as e:
        logging.error(f"Error during analysis: {e}", exc_info=True)
        return {"error": str(e)}
