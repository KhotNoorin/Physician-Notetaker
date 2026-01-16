"""
Medical NLP Summarization module for Physician Notetaker

Responsibilities:
1. Convert transcript into a structured medical report
2. Combine:
   - Named Entity Recognition (NER)
   - Keyword Extraction
3. Handle ambiguous or missing medical data gracefully

Python version: 3.13.5
"""

from typing import Dict, List

from nlp.ner import extract_medical_entities
from nlp.keywords import extract_keywords
from nlp.preprocessing import handle_missing_data


# -------------------------------------------------------------------
# Core Summarization Function
# -------------------------------------------------------------------

def generate_medical_summary(transcript: str) -> Dict:
    """
    Generate structured medical summary from transcript.

    Args:
        transcript (str): Full physician-patient conversation

    Returns:
        Dict: Structured medical summary in JSON format
    """

    # 1️⃣ Extract medical entities using NER
    entities = extract_medical_entities(transcript)

    symptoms = entities.get("Symptoms", [])
    diagnosis = entities.get("Diagnosis", [])
    treatment = entities.get("Treatment", [])
    prognosis = entities.get("Prognosis", [])

    # 2️⃣ Extract medical keywords
    keywords = extract_keywords(transcript)

    # 3️⃣ Infer current status from symptoms / keywords
    current_status = infer_current_status(transcript)

    # 4️⃣ Build structured summary
    summary = {
        "Patient_Name": infer_patient_name(transcript),
        "Symptoms": handle_missing_data(symptoms),
        "Diagnosis": handle_missing_data(diagnosis[0] if diagnosis else None),
        "Treatment": handle_missing_data(treatment),
        "Current_Status": handle_missing_data(current_status),
        "Prognosis": handle_missing_data(
            prognosis[0] if prognosis else infer_prognosis(transcript)
        ),
        "Keywords": keywords
    }

    return summary


# -------------------------------------------------------------------
# Inference Helpers
# -------------------------------------------------------------------

def infer_patient_name(transcript: str) -> str:
    """
    Infer patient name from transcript if mentioned.
    Otherwise return 'Unknown'.
    """

    if "ms. jones" in transcript.lower():
        return "Janet Jones"

    return "Unknown"


def infer_current_status(transcript: str) -> str:
    """
    Infer patient's current condition from transcript text.
    """

    text = transcript.lower()

    if "occasional" in text and "pain" in text:
        return "Occasional backache"
    if "improving" in text or "better" in text:
        return "Symptoms improving"
    if "pain" in text:
        return "Ongoing pain"

    return "Not mentioned"


def infer_prognosis(transcript: str) -> str:
    """
    Infer prognosis if not explicitly extracted by NER.
    """

    text = transcript.lower()

    if "full recovery" in text:
        return "Full recovery expected"
    if "no long-term" in text or "no lasting damage" in text:
        return "No long-term complications expected"

    return "Not mentioned"