// ============================================================
// App
// Top-level component. Holds simple page state ("main" or
// "results") and renders the shared header/footer around the
// active page. No router needed for a two-page prototype.
// ============================================================

import { useState } from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import MainPage from './components/MainPage'
import ResultsPage from './components/ResultsPage'
import type { BiasReport } from './types'

type PageName = 'main' | 'results'

function App() {
  const [page, setPage] = useState<PageName>('main')
  const [report, setReport] = useState<BiasReport | null>(null)

  return (
    <div className="min-h-screen bg-[#E2E2E2]">
      <Header
        title={page === 'main' ? 'University CV Bias Toolkit' : 'Bias Report'}
      />

      {page === 'main' || !report ? (
        <MainPage
          onGenerate={(generated) => {
            setReport(generated)
            setPage('results')
          }}
        />
      ) : (
        <ResultsPage report={report} onBack={() => setPage('main')} />
      )}

      <Footer />
    </div>
  )
}

export default App
