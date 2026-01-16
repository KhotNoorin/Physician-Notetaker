"""
Validation utilities for Physician Notetaker

Provides:
- Conversation schema validation
- NLP output validation
- Medical field checks

Python version: 3.13.5
"""

from typing import List, Dict


# -------------------------------------------------------------------
# Conversation Validation
# -------------------------------------------------------------------

def validate_conversation(conversation: List[Dict]) -> bool:
    """
    Validate conversation structure.

    Each entry must contain:
    - role (Patient or Physician)
    - text (non-empty string)
    """

    if not isinstance(conversation, list):
        return False

    for entry in conversation:
        if not isinstance(entry, dict):
            return False

        if entry.get("role") not in {"Patient", "Physician"}:
            return False

        text = entry.get("text")
        if not isinstance(text, str) or not text.strip():
            return False

    return True


# -------------------------------------------------------------------
# Summary Validation
# -------------------------------------------------------------------

def validate_structured_summary(summary: Dict) -> bool:
    """
    Validate structured medical summary JSON.
    """

    required_fields = {
        "Patient_Name",
        "Symptoms",
        "Diagnosis",
        "Treatment",
        "Current_Status",
        "Prognosis"
    }

    if not isinstance(summary, dict):
        return False

    missing = required_fields - summary.keys()
    if missing:
        return False

    return True


# -------------------------------------------------------------------
# Sentiment & Intent Validation
# -------------------------------------------------------------------

def validate_sentiment_intent(sentiment: str, intent: str) -> bool:
    """
    Validate sentiment and intent values.
    """

    valid_sentiments = {"Anxious", "Neutral", "Reassured"}

    if sentiment not in valid_sentiments:
        return False

    if not isinstance(intent, str) or not intent.strip():
        return False

    return True


# -------------------------------------------------------------------
# SOAP Note Validation
# -------------------------------------------------------------------

def validate_soap_note(soap_note: Dict) -> bool:
    """
    Validate SOAP note structure.
    """

    required_sections = {
        "Subjective",
        "Objective",
        "Assessment",
        "Plan"
    }

    if not isinstance(soap_note, dict):
        return False

    if not required_sections.issubset(soap_note.keys()):
        return False

    return True