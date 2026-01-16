"""
Keyword Extraction module for Physician Notetaker

Extracts important medical keywords and key phrases
from conversation transcripts.

Approach:
- spaCy noun chunks
- Rule-based filtering for medical relevance

Python version: 3.13.5
"""

from typing import List
import spacy

# Load spaCy English model
# Run once: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")


# -------------------------------------------------------------------
# Medical Relevance Vocabulary
# -------------------------------------------------------------------

MEDICAL_KEY_TERMS = {
    "pain",
    "injury",
    "accident",
    "whiplash",
    "physiotherapy",
    "treatment",
    "recovery",
    "back",
    "neck",
    "head",
    "spine",
    "muscle",
    "therapy",
    "painkillers",
    "analgesics",
    "examination"
}


# -------------------------------------------------------------------
# Core Keyword Extraction
# -------------------------------------------------------------------

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract medically relevant keywords and phrases.

    Args:
        text (str): Full transcript text
        max_keywords (int): Maximum number of keywords to return

    Returns:
        List[str]: List of extracted keywords
    """

    if not text:
        return []

    doc = nlp(text.lower())

    keywords = set()

    # 1️⃣ Extract noun chunks
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip()

        # Check if chunk contains medical terms
        if any(term in chunk_text for term in MEDICAL_KEY_TERMS):
            keywords.add(chunk_text)

    # 2️⃣ Extract standalone medical tokens
    for token in doc:
        if token.text in MEDICAL_KEY_TERMS:
            keywords.add(token.text)

    # Normalize and limit output
    normalized = normalize_keywords(list(keywords))

    return normalized[:max_keywords]


# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------

def normalize_keywords(keywords: List[str]) -> List[str]:
    """
    Normalize keywords:
    - Remove duplicates
    - Title case
    - Remove very short phrases
    """

    cleaned = set()

    for kw in keywords:
        kw = kw.strip()
        if len(kw) < 3:
            continue
        cleaned.add(kw.title())

    return sorted(cleaned)