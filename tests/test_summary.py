"""
Unit tests for Medical NLP Summarization

Tests:
- Structured medical summary generation
- Presence of required medical fields

Run using:
pytest tests/test_summary.py

Python version: 3.13.5
"""

from nlp.summarization import generate_medical_summary


def test_generate_medical_summary_structure():
    """
    Test structured medical summary generation.
    """

    transcript = """
    Physician: How are you feeling today?
    Patient: I was in a car accident and had neck and back pain for four weeks.
    Physician: Did you receive treatment?
    Patient: Yes, I completed ten physiotherapy sessions and took painkillers.
    Physician: How are you feeling now?
    Patient: I feel better now with only occasional backache.
    Physician: I expect a full recovery within six months.
    """

    summary = generate_medical_summary(transcript)

    # -------- Required Fields --------
    required_fields = {
        "Patient_Name",
        "Symptoms",
        "Diagnosis",
        "Treatment",
        "Current_Status",
        "Prognosis"
    }

    assert isinstance(summary, dict)
    assert required_fields.issubset(summary.keys())

    # -------- Field Content Checks --------
    assert isinstance(summary["Symptoms"], list)
    assert "Neck Pain" in summary["Symptoms"] or "Back Pain" in summary["Symptoms"]

    assert isinstance(summary["Treatment"], list)
    assert any(
        t in summary["Treatment"]
        for t in ["Physiotherapy", "Painkillers"]
    )

    assert isinstance(summary["Current_Status"], str)
    assert isinstance(summary["Prognosis"], str)
