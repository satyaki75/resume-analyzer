import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
            temperature=0
        )

    def basic_test(self, resume_text: str, job_description: str) -> dict:
        import json
        import re

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
    You are an AI Resume Analyzer.

    Return ONLY valid JSON.
    No explanation, no extra text.

    JSON FORMAT:
    {{
    "candidate_summary": "",
    "job_summary": "",
    "fit_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "red_flags": [],
    "recommendations": {{
        "resume_improvements": [],
        "job_fit_improvements": []
    }},
    "final_verdict": "",
    "confidence": 0.0
    }}
    """
            ),
            (
                "human",
                """
    RESUME:
    {resume}

    JOB:
    {job}
    """
            ),
        ])

        chain = prompt | self.llm

        response = chain.invoke({
            "resume": resume_text,
            "job": job_description
        })

        raw_output = response.content

        # 👇 extract JSON
        match = re.search(r"\{.*\}", raw_output, re.DOTALL)

        if not match:
            raise ValueError("No JSON found")

        json_str = match.group(0)

        # 👇 convert to dict
        return json.loads(json_str)