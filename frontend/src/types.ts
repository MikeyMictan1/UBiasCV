// Shape of the bias report returned by the backend.
// Mirrors backend/BiasAI/models.py (BiasReport).

export interface FlaggedPhrase {
  phrase: string
  reason: string
  evidence_snippet: string
  confidence: string
}

export interface TailoringContext {
  user_role: string
  ai_tool: string
  domain: string
  domain_rubric: string
  tool_profile: string
  gendered_language: string
  review_depth: string
}

export interface BiasReport {
  score: number
  summary: string
  flagged_phrases: FlaggedPhrase[]
  next_steps: string
  tailoring_context: TailoringContext
}
