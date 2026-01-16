"""
Sentiment & Intent Analysis module for Physician Notetaker

Detects:
- Avoidant or anxious sentiment
- Neutral reporting
- Reassured emotional state

Designed for:
- Rule-based inference (current)
- Transformer-based fine-tuning (future)

Python version: 3.13.5
"""

from typing import Dict


# -------------------------------------------------------------------
# Keyword Sets (Lightweight Baseline)
# -------------------------------------------------------------------

ANXIOUS_KEYWORDS = {
    "worried", "scared", "anxious", "concerned", "pain",
    "afraid", "trouble", "difficulty"
}

REASSURED_KEYWORDS = {
    "better", "relief", "fine", "okay", "good",
    "improving", "recovered", "happy"
}

NEUTRAL_KEYWORDS = {
    "had", "experienced", "noticed", "went",
    "received", "took"
}


INTENT_KEYWORDS = {
    "Seeking reassurance": {
        "worried", "hope", "concerned", "afraid"
    },
    "Reporting symptoms": {
        "pain", "hurt", "ache", "discomfort", "stiff"
    },
    "Expressing concern": {
        "trouble", "difficulty", "problem"
    },
    "Reporting improvement": {
        "better", "improving", "relief"
    }
}


# -------------------------------------------------------------------
# Core Analysis Function
# -------------------------------------------------------------------

def analyze_sentiment_and_intent(patient_text: str) -> Dict:
    """
    Analyze patient sentiment and intent from dialogue.

    Args:
        patient_text (str): Concatenated patient utterances

    Returns:
        Dict with keys:
        - Sentiment
        - Intent
    """

    text = patient_text.lower()

    sentiment = detect_sentiment(text)
    intent = detect_intent(text)

    return {
        "Sentiment": sentiment,
        "Intent": intent
    }


# -------------------------------------------------------------------
# Sentiment Detection
# -------------------------------------------------------------------

def detect_sentiment(text: str) -> str:
    """
    Classify sentiment into:
    - Anxious
    - Neutral
    - Reassured
    """

    if any(word in text for word in ANXIOUS_KEYWORDS):
        return "Anxious"

    if any(word in text for word in REASSURED_KEYWORDS):
        return "Reassured"

    return "Neutral"


# -------------------------------------------------------------------
# Intent Detection
# -------------------------------------------------------------------

def detect_intent(text: str) -> str:
    """
    Identify patient intent based on keyword patterns.
    """

    for intent, keywords in INTENT_KEYWORDS.items():
        if any(word in text for word in keywords):
            return intent

    return "Reporting symptoms"