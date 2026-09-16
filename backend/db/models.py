from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Contract(Base):
    __tablename__ = "contracts"

    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    raw_text = Column(Text, nullable=False)

    clauses = relationship("Clause", back_populates="contract")
    summaries = relationship("Summary", back_populates="contract")

class Clause(Base):
    __tablename__ = "clauses"

    clause_id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contracts.contract_id"), nullable=False)
    clause_text = Column(Text, nullable=False)
    clause_type = Column(String, nullable=False)

    contract = relationship("Contract", back_populates="clauses")
    risk_score = relationship("RiskScore", back_populates="clause", uselist=False)

class RiskScore(Base):
    __tablename__ = "risk_scores"

    score_id = Column(Integer, primary_key=True, autoincrement=True)
    clause_id = Column(Integer, ForeignKey("clauses.clause_id"), nullable=False)
    risk_level = Column(String, nullable=False)

    clause = relationship("Clause", back_populates="risk_score")

class Summary(Base):
    __tablename__ = "summaries"

    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contracts.contract_id"), nullable=False)
    summary_text = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

    contract = relationship("Contract", back_populates="summaries")

DATABASE_URL = "sqlite:///lexicore.db"
engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")