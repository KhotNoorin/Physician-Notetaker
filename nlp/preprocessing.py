"""
Preprocessing utilities for Physician Notetaker NLP pipeline

Handles:
- Text normalization
- Speaker separation
- Missing / ambiguous data handling
- Transcript formatting

Python version: 3.13.5
"""

import re
from typing import List, Dict


# -------------------------------------------------------------------
# Core Preprocessing Functions
# -------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Normalize medical text by:
    - Lowercasing
    - Removing extra whitespace
    - Standardizing punctuation
    """

    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)           # collapse whitespace
    text = re.sub(r"[^\w\s.,]", "", text)      # keep basic punctuation

    return text.strip()


def split_by_speaker(transcript: str) -> List[Dict]:
    """
    Split raw transcript into speaker-tagged segments.

    Expected format:
        Physician: ...
        Patient: ...

    Returns:
        List of dicts with 'role' and 'text'
    """

    conversation = []

    lines = transcript.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.lower().startswith("physician:"):
            conversation.append({
                "role": "Physician",
                "text": normalize_text(line.replace("Physician:", "", 1))
            })

        elif line.lower().startswith("patient:"):
            conversation.append({
                "role": "Patient",
                "text": normalize_text(line.replace("Patient:", "", 1))
            })

        else:
            # Ambiguous speaker — assign to patient by default
            conversation.append({
                "role": "Patient",
                "text": normalize_text(line)
            })

    return conversation


def extract_patient_sentences(conversation: List[Dict]) -> str:
    """
    Extract only patient utterances.

    Used for:
    - Sentiment analysis
    - Intent detection
    """

    patient_text = [
        entry["text"]
        for entry in conversation
        if entry.get("role") == "Patient"
    ]

    return " ".join(patient_text)


def extract_physician_sentences(conversation: List[Dict]) -> str:
    """
    Extract physician utterances.

    Useful for:
    - SOAP Objective section
    - Treatment & diagnosis context
    """

    physician_text = [
        entry["text"]
        for entry in conversation
        if entry.get("role") == "Physician"
    ]

    return " ".join(physician_text)


# -------------------------------------------------------------------
# Handling Missing & Ambiguous Medical Data
# -------------------------------------------------------------------

def handle_missing_data(value, placeholder: str = "Not mentioned"):
    """
    Standardize missing medical fields.

    Example:
        None → "Not mentioned"
        [] → "Not mentioned"
    """

    if value is None:
        return placeholder

    if isinstance(value, list) and not value:
        return placeholder

    if isinstance(value, str) and not value.strip():
        return placeholder

    return value


def resolve_ambiguity(entity_list: List[str]) -> List[str]:
    """
    Handle ambiguous or overlapping medical entities.

    Strategy:
    - Remove duplicates
    - Normalize phrasing
    """

    resolved = set()
    for entity in entity_list:
        cleaned = entity.strip().title()
        if cleaned:
            resolved.add(cleaned)

    return list(resolved)


# -------------------------------------------------------------------
# Formatting Helpers
# -------------------------------------------------------------------

def build_transcript_string(conversation: List[Dict]) -> str:
    """
    Convert conversation list into formatted transcript string.
    """

    lines = [
        f'{entry["role"]}: {entry["text"]}'
        for entry in conversation
    ]
    return "\n".join(lines)