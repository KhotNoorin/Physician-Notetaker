"""
Unit tests for Medical Named Entity Recognition (NER)

Run using:
pytest tests/test_ner.py
"""

import sys
import os

# Add project root to PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from nlp.ner import extract_medical_entities


def test_medical_ner_extraction():
    """
    Test medical entity extraction from sample transcript.
    """

    transcript = """
    Patient: I was in a car accident.
    Patient: I had severe neck and back pain for four weeks.
    Patient: Doctors said it was a whiplash injury.
    Patient: I took painkillers and completed physiotherapy sessions.
    Patient: I am feeling better now and expect a full recovery.
    """

    entities = extract_medical_entities(transcript)

    assert "Neck Pain" in entities["Symptoms"]
    assert "Back Pain" in entities["Symptoms"]
    assert "Whiplash Injury" in entities["Diagnosis"]
    assert "Painkillers" in entities["Treatment"]
    assert "Physiotherapy" in entities["Treatment"]
    assert "Full Recovery" in entities["Prognosis"]