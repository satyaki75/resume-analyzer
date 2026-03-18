from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
import os
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.services.parser_service import extract_text
from app.services.llm_service import LLMService
from app.services.embedding_service import get_embedding

from app.db.database import get_db
from app.db.models import Analysis


router = APIRouter()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf", ".docx"]

# initialize once
llm_service = LLMService()


# =========================
# 🚀 ANALYZE ENDPOINT
# =========================
@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)   # ✅ added DB session
):
    try:
        # validate filename
        if not file.filename:
            raise HTTPException(status_code=400, detail="Invalid file")

        ext = os.path.splitext(file.filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are allowed"
            )

        # generate unique filename
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(TEMP_DIR, unique_filename)

        # save file
        content = await file.read()

        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        with open(file_path, "wb") as f:
            f.write(content)

        # extract text
        resume_text = extract_text(file_path, ext)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from file"
            )

        # ✅ Generate embeddings
        resume_embedding = get_embedding(resume_text)
        job_embedding = get_embedding(job_description)

        # sanity check
        print("Resume embedding length:", len(resume_embedding))
        print("Job embedding length:", len(job_embedding))

        # LLM call
        llm_output = llm_service.basic_test(resume_text, job_description)

        # ✅ STORE IN DB
        analysis = Analysis(
            resume_text=resume_text,
            job_description=job_description,
            fit_score=llm_output.get("fit_score"),
            analysis_json=str(llm_output),  # store as string
            resume_embedding=resume_embedding,
            job_embedding=job_embedding
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return {
            "message": "Analysis generated",
            "analysis_id": analysis.id,
            "raw_output": llm_output,
            "embedding_info": {
                "resume_embedding_dim": len(resume_embedding),
                "job_embedding_dim": len(job_embedding)
            }
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# =========================
# 🔍 SIMILARITY SEARCH
# =========================
@router.post("/similar")
async def find_similar_resumes(
    query_text: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # generate embedding
        query_embedding = get_embedding(query_text)

        # execute similarity search (FIXED with CAST)
        results = db.execute(
            text("""
                SELECT id, fit_score, analysis_json
                FROM analysis
                ORDER BY resume_embedding <=> CAST(:embedding AS vector)
                LIMIT 5
            """),
            {"embedding": query_embedding}
        ).fetchall()

        # format response
        formatted_results = [
            {
                "id": row[0],
                "fit_score": row[1],
                "analysis": row[2]
            }
            for row in results
        ]

        return {"results": formatted_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{analysis_id}")
async def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    try:
        obj = db.query(Analysis).filter(Analysis.id == analysis_id).first()

        if not obj:
            raise HTTPException(status_code=404, detail="Candidate not found")

        db.delete(obj)
        db.commit()

        return {"message": f"Candidate {analysis_id} deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))