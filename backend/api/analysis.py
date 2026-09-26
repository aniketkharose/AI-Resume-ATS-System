from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.services.resume_analyzer import analyze_resume
from backend.services.jd_parser import (
    process_job_description,
)
from backend.services.skill_extractor import (
    SKILL_DATABASE,
)
from backend.services.hybrid_matcher import (
    HybridMatcher,
)
from backend.services.ats_scorer import (
    calculate_ats_score,
)
from backend.services.feedback_engine import (
    generate_feedback,
)
from backend.services.recommendation_engine import (
    generate_recommendations,
)


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post("/analyze")
async def analyze_resume_endpoint(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    use_groq: bool = Form(True),
) -> dict[str, Any]:
    """
    Analyze a resume against a job description.

    Pipeline:

    Resume
       ↓
    Resume Analyzer
       ↓
    JD Parser
       ↓
    Hybrid Matcher
       ↓
    ATS Scorer
       ↓
    Feedback
       ↓
    Recommendations
    """

    # ========================================================
    # 1. Validate JD
    # ========================================================

    if not job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    # ========================================================
    # 2. Validate file
    # ========================================================

    if not resume.filename:

        raise HTTPException(
            status_code=400,
            detail="Resume filename is required.",
        )

    allowed_extensions = {
        ".pdf",
        ".docx",
    }

    filename_lower = resume.filename.lower()

    if not any(
        filename_lower.endswith(ext)
        for ext in allowed_extensions
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported resume format. "
                "Only PDF and DOCX are supported."
            ),
        )

    # ========================================================
    # 3. Read uploaded resume
    # ========================================================

    try:

        file_data = await resume.read()

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=f"Unable to read uploaded file: {exc}",
        )

    if not file_data:

        raise HTTPException(
            status_code=400,
            detail="Uploaded resume is empty.",
        )

    # ========================================================
    # 4. Resume analysis
    # ========================================================

    try:

        resume_analysis = analyze_resume(
            file_data=file_data,
            filename=resume.filename,
            content_type=resume.content_type,
            use_groq=use_groq,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=422,
            detail=f"Resume analysis failed: {exc}",
        )

    # ========================================================
    # 5. Parse Job Description
    # ========================================================

    try:

        jd_result = process_job_description(
            job_description,
            SKILL_DATABASE,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=422,
            detail=f"Job description parsing failed: {exc}",
        )

    # ========================================================
    # 6. Hybrid matching
    # ========================================================

    try:

        matcher = HybridMatcher(
            semantic_threshold=0.65,
            related_threshold=0.45,
        )

        hybrid_result = matcher.match(
            resume_skills=resume_analysis["skills"],
            jd_skills=jd_result["skills"],
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Skill matching failed: {exc}",
        )

    # ========================================================
    # 7. ATS score
    # ========================================================

    try:

        ats_result = calculate_ats_score(
            resume_analysis=resume_analysis,
            hybrid_result=hybrid_result,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"ATS scoring failed: {exc}",
        )

    # ========================================================
    # 8. Feedback
    # ========================================================

    try:

        feedback = generate_feedback(
            resume_analysis=resume_analysis,
            hybrid_result=hybrid_result,
            ats_result=ats_result,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Feedback generation failed: {exc}",
        )

    # ========================================================
    # 9. Recommendations
    # ========================================================

    try:

        recommendations = generate_recommendations(
            resume_analysis=resume_analysis,
            hybrid_result=hybrid_result,
            ats_result=ats_result,
            feedback=feedback,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Recommendation generation failed: {exc}"
            ),
        )

    # ========================================================
    # 10. Final API response
    # ========================================================

    return {
        "success": True,

        "resume": {
            "filename": resume.filename,
            "content_type": resume.content_type,
        },

        "job_description": {
            "skills": jd_result["skills"],
            "sections": jd_result.get(
                "sections",
                {},
            ),
        },

        "resume_analysis": resume_analysis,

        "matching": hybrid_result,

        "ats": ats_result,

        "feedback": feedback,

        "recommendations": recommendations,
    }