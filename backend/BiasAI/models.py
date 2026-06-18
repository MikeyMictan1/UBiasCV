# Pydantic schemas for the bias report.
# These mirror claude_output_template.json and are used both to constrain
# Claude's structured output and as the FastAPI response model.

from pydantic import BaseModel


class FlaggedPhrase(BaseModel):
    phrase: str
    reason: str


class BiasReport(BaseModel):
    # 0 = no detectable bias, 100 = severe, pervasive bias
    score: float
    summary: str
    flagged_phrases: list[FlaggedPhrase]
    next_steps: str
