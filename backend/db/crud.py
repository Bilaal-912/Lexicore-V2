from sqlalchemy.orm import sessionmaker
from backend.db.models import engine, Contract, Clause, RiskScore, Summary

Session = sessionmaker(bind=engine)

def save_contract(filename: str, raw_text: str, clauses_data: list[dict], summary_text: str) -> int:
    session = Session()

    contract = Contract(filename=filename, raw_text=raw_text)
    session.add(contract)
    session.flush()

    for clause_data in clauses_data:
        clause = Clause(
            contract_id=contract.contract_id,
            clause_text=clause_data["text"],
            clause_type=clause_data["category"]
        )
        session.add(clause)
        session.flush()

        risk_score = RiskScore(
            clause_id=clause.clause_id,
            risk_level=clause_data["risk"]
        )
        session.add(risk_score)

    summary = Summary(contract_id=contract.contract_id, summary_text=summary_text)
    session.add(summary)

    session.commit()
    contract_id = contract.contract_id
    session.close()

    return contract_id