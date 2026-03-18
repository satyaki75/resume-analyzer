# 🚀 AI Resume Analyzer + Job Fit Scorer

AI Resume Analyzer is a full-stack application that leverages large language models and vector embeddings to intelligently evaluate candidate resumes against job descriptions. It provides deep analytical insights, including fit scores, skill matching, strengths/weaknesses identification, and actionable recommendations. Additionally, it features an AI memory system to retrieve similar past candidates using vector similarity search.

---

## ✨ Features

- **Automated Resume Parsing**: Extracts and cleans text from both `.pdf` and `.docx` formats.
- **Deep AI Analysis**: Utilizes **Groq's LLaMA 3.3 70B** via LangChain to deeply analyze the semantic match between a resume and a job description.
- **Comprehensive Grading**: Generates a fit score, confidence metric, matched/missing skills, strengths, weaknesses, red flags, and tailored recommendations.
- **AI Memory & Candidate Retrieval**: Calculates document embeddings using `SentenceTransformers (all-MiniLM-L6-v2)` and stores them in a **PostgreSQL** database using `pgvector`. Allows for semantic retrieval of similar candidates based on new job descriptions.
- **Sleek Interface**: Includes a responsive **Streamlit** front-end for uploading resumes, pasting job descriptions, and visualizing the analysis results.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL (with [pgvector](https://github.com/pgvector/pgvector) for vector similarity search)
- **ORM**: SQLAlchemy
- **AI/LLM**: [Groq API](https://groq.com/) (LLaMA 3.3 70B model)
- **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2`) via Hugging Face
- **Framework & Parsing**: LangChain (`PyPDFLoader`, `Docx2txtLoader`)

### Frontend
- **Framework**: [Streamlit](https://streamlit.io/)
- **Communication**: Requests (REST API interactions)

---

## 📂 Project Structure

```text
resume-analyzer/
├── backend/
│   ├── app/
│   │   ├── core/              # Core configurations
│   │   ├── db/                # Database setup (database.py) and SQLAlchemy Models (models.py)
│   │   ├── routes/            # API endpoints (analyze.py)
│   │   ├── services/          # Business logic
│   │   │   ├── embedding_service.py # SentenceTransformer embedding generation
│   │   │   ├── llm_service.py       # LangChain + Groq integration
│   │   │   └── parser_service.py    # PDF & DOCX text extraction
│   │   └── main.py            # FastAPI application entry point
│   ├── req.txt                # Backend specific dependencies
│   └── temp/                  # Temporary directory for file uploads
├── frontend/
│   └── streamlit_ui.py        # Streamlit frontend application
├── pyproject.toml             # Project package definitions
└── README.md                  # Project documentation (this file)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- PostgreSQL database with the `pgvector` extension installed
- Groq API Key
- Hugging Face Token (for SentenceTransformers)

### 1. Database Setup
Ensure you have a running PostgreSQL instance. The application requires a database named `resume_analyzer` (or update `DATABASE_URL` in `backend/app/db/database.py`).
Enable the `vector` extension in your PostgreSQL instance:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Installation
Install the required dependencies defined in the `pyproject.toml` file or backend `req.txt`.

```bash
# Example using pip and the pyproject.toml
pip install .

# Or using requirements text
pip install -r backend/req.txt
```

### 3. Environment Variables
Create a `.env` file in the root configuration (typically required by `llm_service.py` and `embedding_service.py`) and populate it with:
```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

### 4. Running the Application

**Start the FastAPI Backend**:
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
> The API will be available at `http://localhost:8000`, and interactive API docs at `http://localhost:8000/docs`.

**Start the Streamlit Frontend**:
Open a new terminal and run:
```bash
streamlit run frontend/streamlit_ui.py
```
> The UI will automatically pop up in your default web browser (usually at `http://localhost:8501`).

---

## 🔌 API Endpoints

- `POST /analyze`
  - Accepts a resume file (`file`) and a `job_description` string.
  - Extracts text, converts it to embeddings, analyzes fit using LLM, and persists results to PostgreSQL.
  - Returns detailed JSON output with all analysis metrics.

- `POST /similar`
  - Accepts a `query_text` (typically a job description).
  - Uses `pgvector` cosine distance (`<=>`) to find and return the top 5 previously stored candidates who match the semantic intent.

- `DELETE /delete/{analysis_id}`
  - Deletes a specific candidate record from the DB.

---

## 🚀 Deployment (Vercel)

If you plan to deploy the frontend on Vercel or similar platforms, ensure you set the `API_BASE_URL` environment variable to point to your hosted backend URL. The Streamlit UI code already supports overriding the default `http://localhost:8000` base URL via this environment variable.
