# Controller: HTTP boundary for the bias-analysis feature.
# Receives the uploaded files + questionnaire, delegates to the service,
# returns the BiasReport JSON.

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from BiasAI.extract import extract_text
from BiasAI.models import BiasReport
from BiasAI.service import generate_bias_report
from BiasRuleAlgo.rba import run_strategies

router = APIRouter(prefix="/api", tags=["bias"])


@router.post("/analyze", response_model=BiasReport)
async def analyze(
    cv: UploadFile = File(...),
    ai_feedback: UploadFile = File(...),
    user: str = Form(...),
    ai_tool: str = Form(...),
    course: str = Form(...),
    gendered: str = Form(...),
) -> BiasReport:
    cv_text = extract_text(cv)
    feedback_text = extract_text(ai_feedback)

    if not cv_text.strip() or not feedback_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not read text from one of the uploaded files.",
        )

    strategy_results = run_strategies(cv_text, feedback_text)

    questionnaire = {
        "user": user,
        "ai_tool": ai_tool,
        "course": course,
        "gendered": gendered,
    }

    try:
        report = generate_bias_report(
            cv_text,
            feedback_text,
            questionnaire,
            strategy_results,
        )
    except Exception as exc:  # surface API/parse failures to the frontend
        raise HTTPException(status_code=502, detail=f"Claude API error: {exc}")

    if report is None:
        raise HTTPException(
            status_code=502, detail="The model could not produce a report."
        )

    return report
