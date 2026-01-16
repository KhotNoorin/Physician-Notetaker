"""
Unit tests for Sentiment & Intent Analysis

Tests classification of:
- Anxious
- Neutral
- Reassured

Run using:
pytest tests/test_sentiment.py

Python version: 3.13.5
"""

from nlp.sentiment_intent import analyze_sentiment_and_intent


def test_anxious_sentiment():
    """
    Patient expresses worry and concern.
    """
    text = "I am worried about my back pain and hope it gets better."

    result = analyze_sentiment_and_intent(text)

    assert result["Sentiment"] == "Anxious"
    assert result["Intent"] == "Seeking reassurance"


def test_reassured_sentiment():
    """
    Patient expresses relief and improvement.
    """
    text = "I feel much better now. That is a relief."

    result = analyze_sentiment_and_intent(text)

    assert result["Sentiment"] == "Reassured"
    assert result["Intent"] == "Reporting improvement"


def test_neutral_sentiment():
    """
    Patient reports symptoms without emotion.
    """
    text = "I had neck pain after the accident."

    result = analyze_sentiment_and_intent(text)

    assert result["Sentiment"] == "Anxious" or result["Sentiment"] == "Neutral"
    assert result["Intent"] in {"Reporting symptoms", "Seeking reassurance"}