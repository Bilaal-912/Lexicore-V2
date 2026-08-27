import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from backend.nlp.pdf_extractor import extract_text_from_pdf
from backend.nlp.clause_segmenter import clean_text, segment_clauses
from backend.nlp.risk_scorer import get_risk_level

MODEL_PATH = "backend/nlp/model/legal_bert_clause_classifier"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()