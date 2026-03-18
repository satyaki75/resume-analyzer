from pydantic import BaseModel, Field
from typing import List


class Recommendations(BaseModel):
    resume_improvements: List[str] = Field(
        ..., description="Suggestions to improve the resume"
    )
    job_fit_improvements: List[str] = Field(
        ..., description="Suggestions to better match the job description"
    )


class ResumeAnalysisResponse(BaseModel):
    candidate_summary: str = Field(
        ..., description="Summary of the candidate based on resume"
    )
    job_summary: str = Field(
        ..., description="Summary of the job description"
    )

    fit_score: int = Field(
        ..., ge=0, le=100, description="Overall job fit score (0-100)"
    )

    matched_skills: List[str] = Field(
        ..., description="Skills that match the job requirements"
    )
    missing_skills: List[str] = Field(
        ..., description="Important skills missing in the candidate"
    )

    strengths: List[str] = Field(
        ..., description="Candidate strengths relevant to the job"
    )
    weaknesses: List[str] = Field(
        ..., description="Candidate weaknesses or gaps"
    )
    red_flags: List[str] = Field(
        ..., description="Potential concerns or risks"
    )

    recommendations: Recommendations = Field(
        ..., description="Improvement suggestions"
    )

    final_verdict: str = Field(
        ..., description="Final hiring recommendation"
    )

    confidence: float = Field(
        ..., ge=0, le=1, description="Confidence score (0 to 1)"
    )