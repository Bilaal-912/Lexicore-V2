from backend.nlp.pdf_extractor import extract_text_from_pdf
from backend.nlp.clause_segmenter import clean_text, segment_clauses
from backend.nlp.pipeline_test import classify_clause, is_boilerplate
from backend.nlp.risk_scorer import get_risk_level
from backend.nlp.summarizer import summarize_text
from backend.db.crud import save_contract

raw_text = extract_text_from_pdf("data/sample_contract.pdf")
cleaned = clean_text(raw_text)
clauses = segment_clauses(cleaned)

clauses_data = []
for clause in clauses:
    if is_boilerplate(clause):
        category = "Boilerplate/Administrative"
        risk = "Low"
    else:
        category = classify_clause(clause)
        risk = get_risk_level(category, clause)

    clauses_data.append({"text": clause, "category": category, "risk": risk})

summary_text = summarize_text(cleaned, num_sentences=5)

contract_id = save_contract(
    filename="sample_contract.pdf",
    raw_text=raw_text,
    clauses_data=clauses_data,
    summary_text=summary_text
)

print(f"Saved contract with ID: {contract_id}")