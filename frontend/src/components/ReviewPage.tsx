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
  if (score > 40) return '#c49a1b'
  if (score >= 20) return '#cfd147'
  return '#2f9e44'
}

// Score → one-line verdict, aligned with the colour bands.
function scoreLabel(score: number): string {
  if (score > 60) return 'Significant Bias Introduced'
  if (score > 40) return 'Moderate Bias Introduced'
  if (score >= 20) return 'Bias Somewhat Introduced'
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

function ReviewPage({ report }: { report: BiasReport; user: string }) {
  const score = Math.round(report.score)
  const color = scoreColor(score)

  if (!report.input_valid) {
    return (
      <div className="mx-auto w-full max-w-6xl px-4 py-6 sm:px-6 sm:py-8 lg:px-10">
        <p className="mb-4 text-base text-brand">Review</p>

        <div className="border border-[#c49a1b]/40 bg-[#c49a1b]/10 p-6 sm:p-8">
          <h1 className="mb-3 text-2xl font-bold text-[#93650f] sm:text-3xl">
            We couldn't analyze this as a CV and feedback
          </h1>
          <p className="text-base text-ink sm:text-lg">
            {report.input_notice ??
              "The uploaded files don't appear to be a CV and AI feedback on that CV."}
          </p>
          <p className="mt-4 whitespace-pre-line text-base text-bodygray sm:text-lg">
            {report.next_steps}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-6 sm:px-6 sm:py-8 lg:px-10">
      <p className="mb-4 text-base text-brand">Review</p>

      {/* Score */}
      <SectionHeading title="BIAS SCORE" />
      <div className="mb-10 mt-4 flex flex-col items-start gap-2 sm:flex-row sm:flex-wrap sm:items-center sm:justify-between sm:gap-4">
        <span className="text-4xl font-bold sm:text-5xl lg:text-6xl" style={{ color }}>
          {score}/100
        </span>
        <span className="text-2xl font-bold sm:text-3xl lg:text-5xl" style={{ color }}>
          {scoreLabel(score)}
        </span>
      </div>

      {/* Summary */}
      <SectionHeading title="SUMMARY" />
      <p className="mb-10 mt-4 whitespace-pre-line text-base text-bodygray sm:text-lg">
        {report.summary}
      </p>

      {/* Flagged phrases */}
      <SectionHeading title="FLAGGED PHRASES" />
      {report.flagged_phrases.length === 0 ? (
        <p className="mb-10 mt-4 text-base text-bodygray sm:text-lg">No phrases were flagged.</p>
      ) : (
        <ul className="mb-10 mt-4 space-y-4">
          {report.flagged_phrases.map((item, i) => (
            <li key={i} className="border border-ink/15 bg-white p-4 text-base sm:text-lg">
              <div className="flex flex-wrap items-center gap-3">
                <span className="font-semibold text-ink">“{item.phrase}”</span>
                <span className="border border-brand/30 px-2 py-0.5 text-xs uppercase tracking-wider text-brand">
                  {item.confidence} confidence
                </span>
              </div>
              <p className="mt-2 text-bodygray">{item.reason}</p>
            </li>
          ))}
        </ul>
      )}

      {/* Next steps */}
      <SectionHeading title="RECOMMENDED NEXT STEPS" />
      <p className="mt-4 whitespace-pre-line text-base text-bodygray sm:text-lg">
        {report.next_steps}
      </p>
    </div>
  )
}

export default ReviewPage
