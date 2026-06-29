// Shape of the bias report returned by the backend.
// Mirrors backend/BiasAI/models.py (BiasReport).

export interface FlaggedPhrase {
  phrase: string
  reason: string
}

export interface BiasReport {
  score: number
  summary: string
  flagged_phrases: FlaggedPhrase[]
  next_steps: string
}
