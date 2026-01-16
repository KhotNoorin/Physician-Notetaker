"""
Evaluation utilities for Physician Notetaker

This module provides lightweight evaluation methods for:
- Structured medical summarization
- Sentiment & intent classification
- SOAP note generation

These metrics are rule-based and interpretable.
They can be extended later with ROUGE, BLEU, F1, etc.

Python version: 3.13.5
"""

from typing import Dict


# -------------------------------------------------------------------
# Structured Medical Summary Evaluation
# -------------------------------------------------------------------

def evaluate_structured_summary(
    predicted: Dict,
    reference: Dict
) -> Dict:
    """
    Evaluate structured medical summary quality.

    Metrics:
    - Field coverage
    - Exact field match count
    """

    required_fields = {
        "Patient_Name",
        "Symptoms",
        "Diagnosis",
        "Treatment",
        "Current_Status",
        "Prognosis"
    }

    predicted_fields = set(predicted.keys())
    reference_fields = set(reference.keys())

    covered_fields = required_fields & predicted_fields
    coverage_score = len(covered_fields) / len(required_fields)

    exact_matches = 0
    for field in required_fields:
        if field in predicted and field in reference:
            if predicted[field] == reference[field]:
                exact_matches += 1

    return {
        "field_coverage": round(coverage_score, 2),
        "exact_match_count": exact_matches,
        "total_fields": len(required_fields)
    }


# -------------------------------------------------------------------
# Sentiment & Intent Evaluation
# -------------------------------------------------------------------

def evaluate_sentiment_intent(
    predicted_sentiment: str,
    predicted_intent: str,
    reference_sentiment: str,
    reference_intent: str
) -> Dict:
    """
    Evaluate sentiment and intent classification correctness.
    """

    return {
        "sentiment_correct": predicted_sentiment == reference_sentiment,
        "intent_correct": predicted_intent == reference_intent
    }


# -------------------------------------------------------------------
# SOAP Note Evaluation
# -------------------------------------------------------------------

def evaluate_soap_note(
    predicted: Dict,
    reference: Dict
) -> Dict:
    """
    Evaluate SOAP note structure.

    Metrics:
    - Section completeness
    - Structural validity
    """

    required_sections = {
        "Subjective",
        "Objective",
        "Assessment",
        "Plan"
    }

    predicted_sections = set(predicted.keys())
    covered_sections = required_sections & predicted_sections

    completeness_score = len(covered_sections) / len(required_sections)

    return {
        "section_completeness": round(completeness_score, 2),
        "all_sections_present": completeness_score == 1.0
    }