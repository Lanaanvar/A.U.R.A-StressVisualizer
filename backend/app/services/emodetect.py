import os
from typing import Dict
import torch
from transformers import pipeline

class EmotionAnalyzer:
    """A class to handle multi-emotion detection and analysis in text."""
    
    # Primary emotions and their related secondary emotions with influence factors
    EMOTION_CLUSTERS = {
        "joy": {
            "happy": 1.0,
            "excited": 0.9,
            "content": 0.8,
            "pleased": 0.7,
            "cheerful": 0.7,
            "delighted": 0.6,
            "satisfied": 0.6
        },
        "sadness": {
            "sad": 1.0,
            "unhappy": 0.9,
            "depressed": 0.8,
            "heartbroken": 0.7,
            "gloomy": 0.7,
            "miserable": 0.6,
            "lonely": 0.6,
            "disappointed": 0.5
        },
        "anger": {
            "angry": 1.0,
            "frustrated": 0.9,
            "irritated": 0.8,
            "annoyed": 0.7,
            "outraged": 0.7,
            "furious": 0.6,
            "bitter": 0.5
        },
        "fear": {
            "afraid": 1.0,
            "scared": 0.9,
            "anxious": 0.8,
            "worried": 0.8,
            "nervous": 0.7,
            "terrified": 0.6,
            "uneasy": 0.5,
            "insecure": 0.5
        },
        "disgust": {
            "disgusted": 1.0,
            "repulsed": 0.9,
            "revolted": 0.8,
            "horrified": 0.7,
            "disapproving": 0.6
        },
        "surprise": {
            "surprised": 1.0,
            "amazed": 0.9,
            "astonished": 0.8,
            "shocked": 0.7,
            "startled": 0.6
        }
    }

    def __init__(self, model_name: str = 'bhadresh-savani/distilbert-base-uncased-emotion'):
        """Initialize the emotion analyzer with specified model."""
        os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"Device set to use {'GPU' if self.device == 0 else 'CPU'}")  # Add this line for debugging
        self.emotion_detector = pipeline('text-classification', 
                                      model=model_name, 
                                      device=self.device)

    def detect(self, input_text: str, threshold: float = 0.1) -> Dict[str, float]:
        """
        Detect multiple emotions in the input text with derived intensities.
        
        Args:
            input_text: The text to analyze
            threshold: Minimum score threshold for including emotions
            
        Returns:
            Dictionary of emotions and their scores
        """
        # Get base emotion predictions
        results = self.emotion_detector(input_text)
        
        # Generate expanded emotions
        expanded_emotions = {}
        
        for result in results:
            base_emotion = result["label"]
            base_score = result["score"]
            
            # Add related emotions with scaled scores
            if base_emotion in self.EMOTION_CLUSTERS:
                for related_emotion, factor in self.EMOTION_CLUSTERS[base_emotion].items():
                    derived_score = base_score * factor
                    if derived_score >= threshold:
                        expanded_emotions[related_emotion] = round(derived_score, 3)
            
            # Cross-influence between emotion clusters
            # For example, high sadness might trigger some anxiety
            if base_score > 0.5:
                if base_emotion == "sadness":
                    # Add some anxiety and loneliness
                    expanded_emotions["anxious"] = round(base_score * 0.4, 3)
                    expanded_emotions["lonely"] = round(base_score * 0.5, 3)
                elif base_emotion == "fear":
                    # Add some sadness and insecurity
                    expanded_emotions["sad"] = round(base_score * 0.3, 3)
                    expanded_emotions["insecure"] = round(base_score * 0.4, 3)
        
        # Sort by intensity
        sorted_emotions = dict(sorted(expanded_emotions.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True))
        
        return sorted_emotions

# # Example usage
# if __name__ == "__main__":
#     analyzer = EmotionAnalyzer()
    
#     sample_text = """It is a warm, expansive feeling that starts deep in my chest, spreading out like sunshine through every part of me. It is a lightness, as if I could float, carried by a sense of pure joy and connection. My heart feels full, almost as if it's overflowing with happiness, and every breath feels like a celebration. There is a calm, peaceful energy, yet I am buzzing with excitement, like the world is inviting me to dance in the moment, free and unburdened. It is the feeling of everything being right, and I am perfectly where I am meant to be."""
    
#     emotions = analyzer.detect(sample_text)
#     print("Detected emotions and intensities:")
#     for emotion, score in emotions.items():
#         print(f"{emotion}: {score}")