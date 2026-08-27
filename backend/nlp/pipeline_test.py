import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from backend.nlp.pdf_extractor import extract_text_from_pdf
from backend.nlp.clause_segmenter import clean_text, segment_clauses
from backend.nlp.risk_scorer import get_risk_level
import torch.nn.functional as F
MODEL_PATH = "backend/nlp/model/legal_bert_clause_classifier"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

CONFIDENCE_THRESHOLD = 0.5

def classify_clause(clause_text: str) -> str:
    inputs = tokenizer(clause_text, return_tensors="pt", truncation=True, padding=True, max_length=256)

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = F.softmax(outputs.logits, dim=-1)
    confidence, predicted_id = torch.max(probabilities, dim=-1)
    if confidence.item() < CONFIDENCE_THRESHOLD:
        return "Uncategorized"

    return model.config.id2label[predicted_id.item()]

BOILERPLATE_HEADERS = [
    "definitions", "recitals", "notices", "counterparts",
    "entire agreement", "severability", "miscellaneous",
    "headings", "further assurances", "amendments"
]

def is_boilerplate(clause_text: str) -> bool:
    first_line = clause_text.strip().split("\n")[0].lower().rstrip(".")
    return first_line in BOILERPLATE_HEADERS

if __name__ == "__main__":
    raw_text = extract_text_from_pdf("data/sample_contract.pdf")
    cleaned = clean_text(raw_text)
    clauses = segment_clauses(cleaned)

    print(f"Processing {len(clauses)} clauses\n")

    for clause in clauses[:5]:
        if is_boilerplate(clause):
            category = "Boilerplate/Administrative"
            risk = "Low"
        else:
            category = classify_clause(clause)
            risk = get_risk_level(category, clause)

        print(f"Category: {category}")
        print(f"Risk: {risk}")
        print(f"Text: {clause[:150]}")
        print("-" * 60)