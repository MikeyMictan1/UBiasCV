// ============================================================
// ReviewPage
// Page 03. Shows the bias score (coloured by severity), a summary,
// the flagged phrases, and recommended next steps — driven by the
// report returned from the backend.
// ============================================================

import type { BiasReport } from '../types'

// Score → colour band: >60 red, 30–60 dark yellow, <30 green.
function scoreColor(score: number): string {
  if (score > 60) return '#ff5d60'
  if (score >= 30) return '#c49a1b'
  return '#2f9e44'
}

// Score → one-line verdict, aligned with the colour bands.
function scoreLabel(score: number): string {
  if (score > 60) return 'Significant Bias Introduced'
  if (score >= 30) return 'Moderate Bias Introduced'
  return 'Minimal Bias Introduced'
}

// Blue uppercase section label with a full-width rule beneath it.
function SectionHeading({ title }: { title: string }) {
  return (
    <>
      <p className="text-lg tracking-wide text-brand">{title}</p>
      <div className="mt-1 border-b border-ink/25" />
    </>
  )
}

function ReviewPage({ report }: { report: BiasReport }) {
  const score = Math.round(report.score)
  const color = scoreColor(score)

  return (
    <div className="mx-auto w-full max-w-6xl px-10 py-8">
      <p className="mb-4 text-base text-brand">Review</p>

      {/* Score */}
      <SectionHeading title="BIAS SCORE" />
      <div className="mb-10 mt-4 flex flex-wrap items-center justify-between gap-4">
        <span className="text-6xl font-bold" style={{ color }}>
          {score}/100
        </span>
        <span className="text-5xl font-bold" style={{ color }}>
          {scoreLabel(score)}
        </span>
      </div>

      {/* Summary */}
      <SectionHeading title="SUMMARY" />
      <p className="mb-10 mt-4 whitespace-pre-line text-lg text-bodygray">
        {report.summary}
      </p>

      {/* Flagged phrases */}
      <SectionHeading title="FLAGGED PHRASES" />
      {report.flagged_phrases.length === 0 ? (
        <p className="mb-10 mt-4 text-lg text-bodygray">No phrases were flagged.</p>
      ) : (
        <ul className="mb-10 mt-4 space-y-4">
          {report.flagged_phrases.map((item, i) => (
            <li key={i} className="flex gap-3 text-lg">
              <span className="text-ink">•</span>
              <p>
                <span className="font-semibold text-ink">“{item.phrase}”</span>
                <span className="ml-3 text-bodygray">{item.reason}</span>
              </p>
            </li>
          ))}
        </ul>
      )}

      {/* Next steps */}
      <SectionHeading title="RECOMMENDED NEXT STEPS" />
      <p className="mt-4 whitespace-pre-line text-lg text-bodygray">
        {report.next_steps}
      </p>
    </div>
  )
}

export default ReviewPage
