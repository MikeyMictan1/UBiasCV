# Pydantic schemas for the bias report.
# These mirror claude_output_template.json and are used both to constrain
# Claude's structured output and as the FastAPI response model.

from pydantic import BaseModel


class TailoringContext(BaseModel):
    user_role: str
    ai_tool: str
    domain: str
    domain_rubric: str
    tool_profile: str
    gendered_language: str
    review_depth: str


class FlaggedPhrase(BaseModel):
    phrase: str
    reason: str
    evidence_snippet: str
    confidence: str


class AnalysisReport(BaseModel):
    # 0 = no detectable bias, 100 = severe, pervasive bias
    score: float
    summary: str
    flagged_phrases: list[FlaggedPhrase]
    next_steps: str


class BiasReport(AnalysisReport):
    tailoring_context: TailoringContext
