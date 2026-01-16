from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
from typing import List, Dict

# -------------------------------
# Project Configuration
# -------------------------------
from config import (
    APP_NAME,
    DEBUG,
    HOST,
    PORT,
    DATA_DIR,
    OUTPUTS_DIR
)

# NLP Pipeline
from nlp.pipeline import run_nlp_pipeline

# Logger
from utils.logger import get_logger

# Validators
from utils.validators import (
    validate_conversation,
    validate_structured_summary,
    validate_sentiment_intent,
    validate_soap_note
)

# -------------------------------
# App Initialization
# -------------------------------
app = Flask(__name__)
app.config["APP_NAME"] = APP_NAME

logger = get_logger(__name__)
logger.info(f"{APP_NAME} application started")

# -------------------------------
# In-memory conversation store
# -------------------------------
conversation_history: List[Dict] = []

# -------------------------------
# File Paths (from config)
# -------------------------------
LOG_FILE = DATA_DIR / "conversation_log.json"

SUMMARY_FILE = OUTPUTS_DIR / "structured_summary.json"
SENTIMENT_FILE = OUTPUTS_DIR / "sentiment_intent.json"
SOAP_FILE = OUTPUTS_DIR / "soap_note.json"

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------

@app.route("/")
def index():
    """
    Render main UI (Physician Notetaker dashboard)
    """
    logger.info("Rendering main dashboard")
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle one turn of patient conversation and run NLP pipeline
    """
    try:
        data = request.get_json(silent=True) or {}
        patient_message = data.get("message", "").strip()

        if not patient_message:
            logger.warning("Empty patient message received")
            return jsonify({"error": "Empty message"}), 400

        # -------------------------------
        # Store patient message
        # -------------------------------
        conversation_history.append({
            "role": "Patient",
            "text": patient_message,
            "timestamp": datetime.utcnow().isoformat()
        })

        if not validate_conversation(conversation_history):
            logger.error("Conversation validation failed")
            return jsonify({"error": "Invalid conversation format"}), 400

        logger.info("Patient message stored and validated")

        # -------------------------------
        # Generate physician reply
        # -------------------------------
        physician_reply = generate_physician_reply(patient_message)

        conversation_history.append({
            "role": "Physician",
            "text": physician_reply,
            "timestamp": datetime.utcnow().isoformat()
        })

        logger.info("Physician reply generated")

        # -------------------------------
        # Run NLP pipeline
        # -------------------------------
        nlp_output = run_nlp_pipeline(conversation_history)
        logger.info("NLP pipeline executed successfully")

        # -------------------------------
        # Validate NLP outputs
        # -------------------------------
        if not validate_structured_summary(nlp_output["summary"]):
            logger.error("Structured summary validation failed")
            return jsonify({"error": "Invalid summary output"}), 500

        if not validate_sentiment_intent(
            nlp_output["sentiment"],
            nlp_output["intent"]
        ):
            logger.error("Sentiment/intent validation failed")
            return jsonify({"error": "Invalid sentiment output"}), 500

        if not validate_soap_note(nlp_output["soap_note"]):
            logger.error("SOAP note validation failed")
            return jsonify({"error": "Invalid SOAP output"}), 500

        logger.info("NLP outputs validated successfully")

        # -------------------------------
        # Persist conversation + outputs
        # -------------------------------
        save_conversation(conversation_history)
        save_nlp_outputs(nlp_output)

        logger.info("Conversation and NLP outputs saved")

        return jsonify({
            "physician_reply": physician_reply,
            "summary": nlp_output["summary"],
            "sentiment": nlp_output["sentiment"],
            "intent": nlp_output["intent"],
            "soap_note": nlp_output["soap_note"]
        })

    except Exception:
        logger.exception("Unhandled error during chat processing")
        return jsonify({"error": "Internal server error"}), 500


# ------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------

def generate_physician_reply(patient_text: str) -> str:
    """
    Rule-based physician response.
    Can be replaced with LLM / dialogue model later.
    """
    text = patient_text.lower()

    if "pain" in text:
        return "Can you tell me more about the location and severity of the pain?"
    elif "accident" in text:
        return "I understand. When did the accident occur, and what injuries did you notice?"
    elif "better" in text or "relief" in text:
        return "That’s good to hear. Are you still experiencing any discomfort?"
    else:
        return "Please continue, I’m listening."


def save_conversation(conversation: List[Dict]) -> None:
    """
    Save conversation history to JSON file
    """
    with LOG_FILE.open("w", encoding="utf-8") as f:
        json.dump(conversation, f, indent=2, ensure_ascii=False)


def save_nlp_outputs(nlp_output: Dict) -> None:
    """
    Save NLP outputs to individual JSON files
    """
    with SUMMARY_FILE.open("w", encoding="utf-8") as f:
        json.dump(nlp_output["summary"], f, indent=2, ensure_ascii=False)

    with SENTIMENT_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "Sentiment": nlp_output["sentiment"],
                "Intent": nlp_output["intent"]
            },
            f,
            indent=2,
            ensure_ascii=False
        )

    with SOAP_FILE.open("w", encoding="utf-8") as f:
        json.dump(nlp_output["soap_note"], f, indent=2, ensure_ascii=False)


# ------------------------------------------------------------------
# App Entry Point
# ------------------------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=DEBUG,
        host=HOST,
        port=PORT
    )