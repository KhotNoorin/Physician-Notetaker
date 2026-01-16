# Medical Summarization Model

This directory is reserved for a trained medical text summarization model.

## Purpose
The summarization model converts long physician–patient
conversations into structured medical summaries, including:
- Symptoms
- Diagnosis
- Treatment
- Current status
- Prognosis

## Planned Models
- facebook/bart-large-cnn
- google/pegasus-pubmed
- T5 / FLAN-T5 (fine-tuned on clinical text)

## Training Data (Future)
- PubMed abstracts
- MIMIC-III / MIMIC-IV clinical notes
- Medical dialogue datasets (e.g., MedDialog)

## Current Status
Summarization is currently implemented using:
- Medical NER
- Keyword extraction
- Rule-based inference

See `nlp/summarization.py` for implementation.