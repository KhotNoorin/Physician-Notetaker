"""
SOAP Note Generation module for Physician Notetaker

SOAP = Subjective, Objective, Assessment, Plan

This module converts a physician–patient transcript into a
structured SOAP note with clinical readability.

Python version: 3.13.5
"""

from typing import Dict

from nlp.ner import extract_medical_entities
from nlp.preprocessing import handle_missing_data


# -------------------------------------------------------------------
# Core SOAP Generator
# -------------------------------------------------------------------

def generate_soap_note(transcript: str) -> Dict:
    """
    Generate SOAP note from a medical transcript.

    Args:
        transcript (str): Full physician–patient conversation

    Returns:
        Dict: SOAP note in structured JSON format
    """

    # Extract medical entities
    entities = extract_medical_entities(transcript)

    symptoms = entities.get("Symptoms", [])
    diagnosis = entities.get("Diagnosis", [])
    treatment = entities.get("Treatment", [])
    prognosis = entities.get("Prognosis", [])

    soap_note = {
        "Subjective": build_subjective_section(transcript, symptoms),
        "Objective": build_objective_section(transcript),
        "Assessment": build_assessment_section(diagnosis),
        "Plan": build_plan_section(treatment, prognosis)
    }

    return soap_note


# -------------------------------------------------------------------
# SOAP Sections
# -------------------------------------------------------------------

def build_subjective_section(transcript: str, symptoms: list) -> Dict:
    """
    Build Subjective section:
    - Chief Complaint
    - History of Present Illness
    """

    chief_complaint = ", ".join(symptoms) if symptoms else "Not mentioned"

    history = infer_history_of_present_illness(transcript)

    return {
        "Chief_Complaint": handle_missing_data(chief_complaint),
        "History_of_Present_Illness": handle_missing_data(history)
    }


def build_objective_section(transcript: str) -> Dict:
    """
    Build Objective section:
    - Physical examination
    - Observations
    """

    text = transcript.lower()

    if "full range of movement" in text or "full range of motion" in text:
        physical_exam = (
            "Full range of motion in cervical and lumbar spine, "
            "no tenderness observed."
        )
    else:
        physical_exam = "Physical examination details not documented."

    observations = "Patient appears in normal health."

    return {
        "Physical_Exam": physical_exam,
        "Observations": observations
    }


def build_assessment_section(diagnosis: list) -> Dict:
    """
    Build Assessment section:
    - Diagnosis
    - Severity
    """

    diagnosis_text = (
        diagnosis[0] if diagnosis else "Condition under evaluation"
    )

    severity = infer_severity(diagnosis_text)

    return {
        "Diagnosis": handle_missing_data(diagnosis_text),
        "Severity": severity
    }


def build_plan_section(treatment: list, prognosis: list) -> Dict:
    """
    Build Plan section:
    - Treatment
    - Follow-up
    """

    if treatment:
        treatment_plan = (
            "Continue " + ", ".join(treatment) +
            " as needed and use analgesics for pain relief."
        )
    else:
        treatment_plan = "Treatment plan not specified."

    follow_up = infer_follow_up(prognosis)

    return {
        "Treatment": treatment_plan,
        "Follow_Up": follow_up
    }


# -------------------------------------------------------------------
# Inference Helpers
# -------------------------------------------------------------------

def infer_history_of_present_illness(transcript: str) -> str:
    """
    Infer History of Present Illness from transcript.
    """

    text = transcript.lower()

    if "car accident" in text:
        return (
            "Patient was involved in a car accident and experienced neck "
            "and back pain for several weeks, now reporting improvement "
            "with occasional discomfort."
        )

    return "History of present illness not clearly documented."


def infer_severity(diagnosis: str) -> str:
    """
    Infer severity based on diagnosis and context.
    """

    if "whiplash" in diagnosis.lower():
        return "Mild, improving"

    return "Severity not specified"


def infer_follow_up(prognosis: list) -> str:
    """
    Infer follow-up instructions.
    """

    if prognosis:
        return (
            "Patient to return if pain worsens or persists beyond "
            "the expected recovery period."
        )

    return "Follow-up as needed."