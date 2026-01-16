"""
NLP Pipeline Orchestrator for Physician Notetaker

Coordinates:
- Preprocessing
- Medical summarization (NER + keywords)
- Sentiment & intent analysis
- SOAP note generation

Python Version: 3.13.5
"""

from typing import List, Dict

from nlp.preprocessing import (
    extract_patient_sentences,
    build_transcript_string
)
from nlp.summarization import generate_medical_summary
from nlp.sentiment_intent import analyze_sentiment_and_intent
from nlp.soap import generate_soap_note


def run_nlp_pipeline(conversation: List[Dict]) -> Dict:
    """
    Run the complete NLP pipeline on the conversation history.

    Args:
        conversation (List[Dict]):
        [
            {"role": "Patient", "text": "..."},
            {"role": "Physician", "text": "..."}
        ]

    Returns:
        Dict containing:
        - summary
        - sentiment
        - intent
        - soap_note
    """

    # 1️ Build transcript
    full_transcript = build_transcript_string(conversation)

    # 2️ Extract patient-only text
    patient_text = extract_patient_sentences(conversation)

    # 3️ Medical NLP summarization
    summary = generate_medical_summary(full_transcript)

    # 4️ Sentiment & intent analysis
    sentiment_intent = analyze_sentiment_and_intent(patient_text)

    # 5️ SOAP note generation
    soap_note = generate_soap_note(full_transcript)

    return {
        "summary": summary,
        "sentiment": sentiment_intent["Sentiment"],
        "intent": sentiment_intent["Intent"],
        "soap_note": soap_note
    }
