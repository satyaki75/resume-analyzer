import streamlit as st
import requests
import os

# --- Config ---
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

ANALYZE_URL = f"{API_BASE_URL}/analyze"
SIMILAR_URL = f"{API_BASE_URL}/similar"

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🚀 AI Resume Analyzer + Job Fit Scorer")

# --- Inputs ---
resume = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
job_desc = st.text_area("Paste Job Description", height=200)

# --- Analyze Button ---
if st.button("Analyze"):

    if not resume or not job_desc:
        st.warning("Please upload a resume and enter job description.")
        st.stop()

    with st.spinner("Analyzing resume..."):

        try:
            # --- CALL ANALYZE API ---
            files = {
                "file": (resume.name, resume.getvalue(), resume.type)
            }

            data = {
                "job_description": job_desc
            }

            response = requests.post(
                ANALYZE_URL,
                files=files,
                data=data,
                timeout=60
            )

            response.raise_for_status()
            response_data = response.json()

            result = response_data.get("raw_output", {})

            if not result:
                st.error("Backend returned empty analysis.")
                st.stop()

        except requests.exceptions.RequestException as e:
            st.error(f"Backend connection failed: {str(e)}")
            st.stop()

        except ValueError:
            st.error("Invalid response from backend.")
            st.stop()

    # --- CALL SIMILAR API ---
    with st.spinner("Fetching similar candidates..."):
        try:
            sim_response = requests.post(
                SIMILAR_URL,
                data={"query_text": job_desc},
                timeout=30
            )

            sim_response.raise_for_status()
            similar_data = sim_response.json().get("results", [])

        except Exception:
            similar_data = []
            st.warning("Could not fetch similar candidates")

    # --- DISPLAY RESULTS ---
    st.success("Analysis Complete ✅")

    # --- Metrics ---
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Fit Score", f"{result.get('fit_score', 0)}%")

    with col2:
        confidence = result.get("confidence", 0)
        st.metric("Confidence", f"{int(confidence * 100)}%")

    st.divider()

    # --- Summaries ---
    st.subheader("🧠 Candidate Summary")
    st.write(result.get("candidate_summary", "N/A"))

    st.subheader("📄 Job Summary")
    st.write(result.get("job_summary", "N/A"))

    st.divider()

    # --- Skills ---
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("✅ Matched Skills")
        for skill in result.get("matched_skills", []):
            st.write(f"- {skill}")

    with col4:
        st.subheader("🚨 Missing Skills")
        for skill in result.get("missing_skills", []):
            st.write(f"- {skill}")

    st.divider()

    # --- Strengths & Weaknesses ---
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("💪 Strengths")
        for s in result.get("strengths", []):
            st.write(f"- {s}")

    with col6:
        st.subheader("⚠️ Weaknesses")
        for w in result.get("weaknesses", []):
            st.write(f"- {w}")

    st.divider()

    # --- Red Flags ---
    st.subheader("🚩 Red Flags")
    for r in result.get("red_flags", []):
        st.write(f"- {r}")

    st.divider()

    # --- Recommendations ---
    st.subheader("📌 Recommendations")

    st.markdown("**Resume Improvements**")
    for r in result.get("recommendations", {}).get("resume_improvements", []):
        st.write(f"- {r}")

    st.markdown("**Job Fit Improvements**")
    for r in result.get("recommendations", {}).get("job_fit_improvements", []):
        st.write(f"- {r}")

    st.divider()

    # --- Final Verdict ---
    st.subheader("🧾 Final Verdict")
    st.write(result.get("final_verdict", "N/A"))

    # =========================
    # 🔥 NEW: SIMILAR CANDIDATES
    # =========================
    st.divider()

    st.subheader("🧠 Similar Candidates (AI Memory)")

    if not similar_data:
        st.info("No similar candidates found yet.")
    else:
        for idx, item in enumerate(similar_data[:3]):
            st.markdown(f"### Candidate {idx+1}")

            st.write(f"**Fit Score:** {item.get('fit_score', 'N/A')}")

            analysis_text = item.get("analysis", "")
            preview = analysis_text[:300] + "..." if analysis_text else "N/A"

            st.write(preview)

            st.divider()