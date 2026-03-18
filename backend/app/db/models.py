from sqlalchemy import Column, Integer, Text, Float, DateTime
from datetime import datetime
from app.db.database import Base
from pgvector.sqlalchemy import Vector

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)

    resume_text = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)

    fit_score = Column(Float)

    analysis_json = Column(Text)  # store full LLM output as string

    created_at = Column(DateTime, default=datetime.utcnow) 
    resume_embedding = Column(Vector(384))

    job_embedding = Column(Vector(384))