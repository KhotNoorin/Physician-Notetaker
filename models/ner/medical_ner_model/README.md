# Medical NER Model

This directory is reserved for a trained Medical Named Entity Recognition (NER) model.

## Intended Use
The model will be used to extract:
- Symptoms
- Diagnosis
- Treatment
- Prognosis

from physician–patient conversations.

## Planned Models
- spaCy custom NER model
- scispaCy (en_core_sci_md)
- BioBERT / ClinicalBERT (via transformers)

## Current Status
Rule-based and spaCy phrase matcher is used in nlp/ner.py
This directory serves as a placeholder for future fine-tuned models.