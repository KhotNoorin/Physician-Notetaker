"""
Unit tests for SOAP Note Generation

Tests:
- SOAP note structure
- Presence of all required sections and key fields

Run using:
pytest tests/test_soap.py

Python version: 3.13.5
"""

from nlp.soap import generate_soap_note


def test_generate_soap_note_structure():
    """
    Test SOAP note generation from a sample transcript.
    """

    transcript = """
    Physician: How are you feeling today?
    Patient: I had a car accident and experienced neck and back pain for four weeks.
    Physician: Did you receive treatment?
    Patient: Yes, I completed physiotherapy sessions and took painkillers.
    Physician: Let us do a physical examination.
    Physician: Your neck and back have a full range of movement with no tenderness.
    Physician: I expect a full recovery within six months.
    """

    soap_note = generate_soap_note(transcript)

    # -------- Top-level SOAP sections --------
    required_sections = {
        "Subjective",
        "Objective",
        "Assessment",
        "Plan"
    }

    assert isinstance(soap_note, dict)
    assert required_sections.issubset(soap_note.keys())

    # -------- Subjective --------
    subjective = soap_note["Subjective"]
    assert "Chief_Complaint" in subjective
    assert "History_of_Present_Illness" in subjective
    assert isinstance(subjective["Chief_Complaint"], str)

    # -------- Objective --------
    objective = soap_note["Objective"]
    assert "Physical_Exam" in objective
    assert "Observations" in objective
    assert isinstance(objective["Physical_Exam"], str)

    # -------- Assessment --------
    assessment = soap_note["Assessment"]
    assert "Diagnosis" in assessment
    assert "Severity" in assessment
    assert isinstance(assessment["Diagnosis"], str)

    # -------- Plan --------
    plan = soap_note["Plan"]
    assert "Treatment" in plan
    assert "Follow_Up" in plan
    assert isinstance(plan["Treatment"], str)