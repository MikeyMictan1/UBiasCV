// ============================================================
// ResultsPage
// Bias report view: overall score banner, a 2x3 grid of result
// cards, and download / back buttons. All values are hardcoded
// placeholders until the backend is connected.
// ============================================================

interface ResultsPageProps {
  onBack: () => void
}

// ---------- Placeholder report data ----------
const REPORT = {
  score: 18,
  summary: 'Significant gender bias introduced.',
}

// Card definitions: title, accent colour, and placeholder content lines
const CARDS = [
  { title: 'Flagged Phrases', color: '#E57373', content: ['-Phrase here'] },
  { title: 'Policy Missed', color: '#EF9A3C', content: [] },
  { title: 'Comparison Summary', color: '#EF9A3C', content: [] },
  { title: 'Bias Patterns Recognised', color: '#E57373', content: [] },
  { title: 'Bias Severity Breakdown', color: '#E57373', content: [] },
  { title: 'Recommended Next Steps', color: '#66BB6A', content: [] },
]

// Single report card: coloured title bar + white content area
interface ReportCardProps {
  title: string
  color: string
  content: string[]
}

function ReportCard({ title, color, content }: ReportCardProps) {
  return (
    <div className="border-4" style={{ borderColor: color }}>
      <div className="px-2 py-1" style={{ backgroundColor: color }}>
        <span className="text-sm font-semibold text-gray-900">{title}</span>
      </div>
      <div className="h-32 bg-white p-2">
        {content.map((line) => (
          <p key={line} className="text-xs text-gray-700">
            {line}
          </p>
        ))}
      </div>
    </div>
  )
}

function ResultsPage({ onBack }: ResultsPageProps) {
  return (
    <main className="mx-auto flex max-w-4xl flex-col items-center px-6 pb-20">
      {/* ---------- Overall score banner ---------- */}
      <div className="mt-4 rounded-sm bg-[#A93215] px-8 py-2">
        <span className="text-3xl font-bold text-white">
          Bias Score: {REPORT.score}/100
        </span>
      </div>
      <p className="mt-2 text-lg text-gray-800">{REPORT.summary}</p>

      {/* ---------- Result cards ---------- */}
      <div className="mt-8 grid w-full grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {CARDS.map((card) => (
          <ReportCard key={card.title} {...card} />
        ))}
      </div>

      {/* ---------- Actions ---------- */}
      <div className="mt-8 flex w-full items-center justify-between">
        <button
          type="button"
          // No backend yet — download is a placeholder
          onClick={() => alert('PDF download not implemented yet.')}
          className="rounded-sm bg-[#4555B5] px-4 py-1.5 text-lg text-white hover:bg-[#3F51A5]"
        >
          Download Report PDF
        </button>
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
