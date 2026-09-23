from fastapi import FastAPI, UploadFile, File
import shutil
import os
from backend.nlp.entity_extractor import truncate_at_exhibits, extract_relevant_entities
from backend.nlp.pdf_extractor import extract_text_from_pdf
from backend.nlp.clause_segmenter import clean_text, segment_clauses
from backend.nlp.pipeline_test import classify_clause, is_boilerplate
from backend.nlp.risk_scorer import get_risk_level
from backend.nlp.summarizer import summarize_text
from backend.db.crud import save_contract
from backend.db.crud import Session
from backend.db.models import Contract

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="LexiCore API")


@app.get("/")
def root():
    return {"message": "LexiCore API is running"}

@app.post("/upload")
def upload_contract(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_text = extract_text_from_pdf(file_path)
    cleaned = clean_text(raw_text)
    cleaned = truncate_at_exhibits(cleaned)
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
    entities = extract_relevant_entities(cleaned)
    contract_id = save_contract(
        filename=file.filename,
        raw_text=raw_text,
        clauses_data=clauses_data,
        summary_text=summary_text
    )

    return {
        "contract_id": contract_id,
        "filename": file.filename,
        "clause_count": len(clauses_data),
        "clauses": clauses_data,
        "summary": summary_text,
        "entities": entities
    }
@app.get("/contracts/{contract_id}")
def get_contract(contract_id: int):
    session = Session()
    contract = session.query(Contract).filter_by(contract_id=contract_id).first()

    if contract is None:
        session.close()
        return {"error": "Contract not found"}

    clauses_data = []
    for clause in contract.clauses:
        clauses_data.append({
            "text": clause.clause_text,
            "category": clause.clause_type,
            "risk": clause.risk_score.risk_level if clause.risk_score else None
        })

    summary_text = contract.summaries[0].summary_text if contract.summaries else None

    session.close()

    return {
        "contract_id": contract.contract_id,
        "filename": contract.filename,
        "upload_date": contract.upload_date,
        "clause_count": len(clauses_data),
        "clauses": clauses_data,
        "summary": summary_text
    }
@app.get("/contracts")
def list_contracts():
    session = Session()
    contracts = session.query(Contract).all()

    result = [
        {
            "contract_id": c.contract_id,
            "filename": c.filename,
            "upload_date": c.upload_date,
            "clause_count": len(c.clauses)
        }
        for c in contracts
    ]

    session.close()
    return result