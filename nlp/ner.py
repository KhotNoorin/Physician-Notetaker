"""
Medical Named Entity Recognition (NER) module
for Physician Notetaker.

Extracts:
- Symptoms
- Diagnosis
- Treatment
- Prognosis

Uses spaCy with rule-based + pattern matching.
Can be upgraded to BioBERT / ClinicalBERT later.

Python version: 3.13.5
"""

from typing import Dict, List
import spacy
from spacy.matcher import PhraseMatcher

# Load spaCy English model
# Run once: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")


# -------------------------------------------------------------------
# Medical Phrase Lists (Rule-Based Seed)
# -------------------------------------------------------------------

SYMPTOM_TERMS = [
    "neck pain",
    "back pain",
    "headache",
    "backache",
    "stiffness",
    "discomfort",
    "pain"
]

DIAGNOSIS_TERMS = [
    "whiplash injury",
    "whiplash",
    "back strain",
    "neck strain"
]

TREATMENT_TERMS = [
    "physiotherapy",
    "painkillers",
    "analgesics",
    "physical therapy",
    "x-ray",
    "x rays"
]

PROGNOSIS_TERMS = [
    "full recovery",
    "recover",
    "improving",
    "no long term damage",
    "no lasting damage"
]


# -------------------------------------------------------------------
# Matcher Setup
# -------------------------------------------------------------------

def build_matcher(terms: List[str]) -> PhraseMatcher:
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(term) for term in terms]
    matcher.add("MEDICAL_TERMS", patterns)
    return matcher


symptom_matcher = build_matcher(SYMPTOM_TERMS)
diagnosis_matcher = build_matcher(DIAGNOSIS_TERMS)
treatment_matcher = build_matcher(TREATMENT_TERMS)
prognosis_matcher = build_matcher(PROGNOSIS_TERMS)


# -------------------------------------------------------------------
# Core NER Function
# -------------------------------------------------------------------

def extract_medical_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract medical entities from transcript text.

    Args:
        text (str): Full conversation transcript

    Returns:
        Dict[str, List[str]]: Medical entities
    """

    doc = nlp(text)

    symptoms = extract_entities(doc, symptom_matcher)
    diagnosis = extract_entities(doc, diagnosis_matcher)
    treatment = extract_entities(doc, treatment_matcher)
    prognosis = extract_entities(doc, prognosis_matcher)

    return {
        "Symptoms": normalize_entities(symptoms),
        "Diagnosis": normalize_entities(diagnosis),
        "Treatment": normalize_entities(treatment),
        "Prognosis": normalize_entities(prognosis)
    }


# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------

def extract_entities(doc, matcher: PhraseMatcher) -> List[str]:
    """
    Apply matcher to document and extract matched phrases.
    """

    matches = matcher(doc)
    entities = []

    for _, start, end in matches:
        span = doc[start:end]
        entities.append(span.text)

    return entities


def normalize_entities(entities: List[str]) -> List[str]:
    """
    Normalize entities:
    - Remove duplicates
    - Title case
    """

    normalized = set()
    for ent in entities:
        ent = ent.strip().title()
        if ent:
            normalized.add(ent)

    return list(normalized)