// ============================================================
// App
// Top-level component. Holds the active page ("intro" | "input" |
// "review"), the selected user role, and the generated report.
// The shared Header (stepper nav) / Footer wrap every page.
// No router needed for a three-page flow.
// ============================================================

import { useState } from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import IntroPage from './components/IntroPage'
import InputDataPage from './components/InputDataPage'
import ReviewPage from './components/ReviewPage'
import type { BiasReport } from './types'

export type PageName = 'intro' | 'input' | 'review'

function App() {
  const [page, setPage] = useState<PageName>('intro')
  const [user, setUser] = useState('')
  const [report, setReport] = useState<BiasReport | null>(null)

  return (
    <div className="flex min-h-screen flex-col bg-beige font-sans text-ink">
      <Header
        page={page}
        canReview={report !== null}
        onNavigate={setPage}
      />

      <main className="flex-1">
        {page === 'intro' && (
          <IntroPage
            onSelectUser={(selected) => {
              setUser(selected)
              setPage('input')
            }}
          />
        )}

        {page === 'input' && (
          <InputDataPage
            user={user}
            onReport={(generated) => {
              setReport(generated)
              setPage('review')
            }}
          />
        )}

        {page === 'review' && report && <ReviewPage report={report} />}
      </main>

      <Footer />
    </div>
  )
}

export default App
