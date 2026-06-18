// ============================================================
// ResultsPage
// Bias report view: overall score banner + scrollable sections
// (summary, flagged phrases, recommended next steps), driven by
// the report returned from the backend.
// ============================================================

import type { BiasReport } from '../types'

interface ResultsPageProps {
  report: BiasReport
  onBack: () => void
}

// One-line verdict based on the bias score
function biasLabel(score: number): string {
  if (score > 80) return 'Significant bias introduced'
  if (score > 60) return 'Considerable bias introduced'
  if (score > 40) return 'Moderate bias introduced'
  if (score > 20) return 'Minor bias introduced'
  return 'Little to no bias detected'
}

// A titled, coloured section in the scrollable report body
interface SectionProps {
  title: string
  color: string
  children: React.ReactNode
}

function Section({ title, color, children }: SectionProps) {
  return (
    <div className="w-full border-l-4 bg-white" style={{ borderColor: color }}>
      <div className="px-3 py-1.5" style={{ backgroundColor: color }}>
        <span className="text-sm font-semibold text-gray-900">{title}</span>
      </div>
      <div className="px-4 py-3 text-sm text-gray-800">{children}</div>
    </div>
  )
}

function ResultsPage({ report, onBack }: ResultsPageProps) {
  return (
    <main className="mx-auto flex max-w-4xl flex-col items-center px-6 pb-20">
      {/* ---------- Overall score banner ---------- */}
      <div className="mt-4 rounded-sm bg-[#A93215] px-8 py-2">
        <span className="text-3xl font-bold text-white">
          Bias Score: {Math.round(report.score)}/100
        </span>
      </div>
      <p className="mt-2 text-lg font-medium text-gray-800">
        {biasLabel(report.score)}
      </p>

      {/* ---------- Scrollable report body ---------- */}
      <div className="mt-6 flex max-h-[60vh] w-full flex-col gap-6 overflow-y-auto pr-2">
        <Section title="Summary" color="#EF9A3C">
          <p className="whitespace-pre-line">{report.summary}</p>
        </Section>

        <Section title="Flagged Phrases" color="#E57373">
          {report.flagged_phrases.length === 0 ? (
            <p className="text-gray-500">No phrases were flagged.</p>
          ) : (
            <ul className="flex flex-col gap-3">
              {report.flagged_phrases.map((item, i) => (
                <li key={i}>
                  <p className="font-semibold text-gray-900">“{item.phrase}”</p>
                  <p className="text-gray-700">{item.reason}</p>
                </li>
              ))}
            </ul>
          )}
        </Section>

        <Section title="Recommended Next Steps" color="#66BB6A">
          <p className="whitespace-pre-line">{report.next_steps}</p>
        </Section>
      </div>

      {/* ---------- Actions ---------- */}
      <div className="mt-8 flex w-full items-center justify-end">
        <button
          type="button"
          onClick={onBack}
          className="rounded-sm bg-gray-400 px-4 py-1.5 text-lg text-gray-900 hover:bg-gray-300"
        >
          Back to Menu
        </button>
      </div>
    </main>
  )
}

export default ResultsPage
