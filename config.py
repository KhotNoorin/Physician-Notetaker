"""
Global configuration file for Physician Notetaker

This file centralizes:
- Application settings
- Directory paths
- NLP configuration
- Model paths
- Logging & evaluation settings

Python version: 3.13.5
"""

from pathlib import Path

# -------------------------------------------------------------------
# Base Project Paths
# -------------------------------------------------------------------

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Data directories
DATA_DIR = BASE_DIR / "data"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
OUTPUTS_DIR = DATA_DIR / "outputs"

# Logs directory
LOGS_DIR = BASE_DIR / "logs"

# Models directory
MODELS_DIR = BASE_DIR / "models"

NER_MODEL_DIR = MODELS_DIR / "ner" / "medical_ner_model"
SENTIMENT_MODEL_PATH = MODELS_DIR / "sentiment" / "bert_sentiment_model.pt"
SUMMARIZATION_MODEL_DIR = MODELS_DIR / "summarization" / "medical_summarizer"

# Ensure directories exist
for directory in [
    DATA_DIR,
    TRANSCRIPTS_DIR,
    OUTPUTS_DIR,
    LOGS_DIR,
    MODELS_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# Application Settings
# -------------------------------------------------------------------

APP_NAME = "Physician Notetaker"
DEBUG = True
HOST = "127.0.0.1"
PORT = 5000

# -------------------------------------------------------------------
# NLP Pipeline Configuration
# -------------------------------------------------------------------

# spaCy settings
SPACY_MODEL = "en_core_web_sm"

# Supported medical entity types
MEDICAL_ENTITY_TYPES = [
    "SYMPTOM",
    "DIAGNOSIS",
    "TREATMENT",
    "PROGNOSIS"
]

# Sentiment labels
SENTIMENT_LABELS = ["Anxious", "Neutral", "Reassured"]

# Intent labels
INTENT_LABELS = [
    "Seeking reassurance",
    "Reporting symptoms",
    "Expressing concern",
    "Reporting improvement"
]

# -------------------------------------------------------------------
# Summarization Configuration
# -------------------------------------------------------------------

# Maximum number of keywords extracted
MAX_KEYWORDS = 10

# Placeholder summarization model name
SUMMARIZATION_MODEL_NAME = "rule_based_v1"

# -------------------------------------------------------------------
# Evaluation Configuration
# -------------------------------------------------------------------

ENABLE_EVALUATION = True

EVALUATION_METRICS = {
    "summarization": ["field_coverage", "exact_match"],
    "sentiment": ["accuracy"],
    "soap": ["section_completeness"]
}

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------

LOG_LEVEL = "INFO"
LOG_FILE_PREFIX = "physician_notetaker"

# -------------------------------------------------------------------
# Security & Privacy (Important for Healthcare)
# -------------------------------------------------------------------

# Mask patient identifiers in logs
MASK_PATIENT_NAMES = True

# Retain conversation logs
SAVE_CONVERSATIONS = True

# -------------------------------------------------------------------
# Future Extensions (Documented)
# -------------------------------------------------------------------

# Speech-to-text
ENABLE_SPEECH_TO_TEXT = False
WHISPER_MODEL_NAME = "base"

# LLM-based physician agent
ENABLE_LLM = False
LLM_PROVIDER = "openai"
LLM_MODEL_NAME = "gpt-4"