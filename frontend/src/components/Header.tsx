// ============================================================
// Header
// Cream top bar: clickable logo (returns to Intro) on the left and
// a three-step stepper nav on the right. The active step is blue
// and underlined; visited/available steps are clickable. Review is
// only reachable once a report has been generated.
// ============================================================

import logoHeader from '../assets/logo-header.png'
import type { PageName } from '../App'

interface HeaderProps {
  page: PageName
  canReview: boolean
  onNavigate: (page: PageName) => void
}

const STEPS: { num: string; label: string; page: PageName }[] = [
  { num: '01', label: 'Introduction', page: 'intro' },
  { num: '02', label: 'Input Data', page: 'input' },
  { num: '03', label: 'Review', page: 'review' },
]

function Header({ page, canReview, onNavigate }: HeaderProps) {
  return (
    <header className="border-b border-ink/40 bg-cream">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-10 py-4">
        {/* Logo → Introduction */}
        <button
          type="button"
          onClick={() => onNavigate('intro')}
          className="shrink-0"
          aria-label="Back to introduction"
        >
          <img src={logoHeader} alt="ubiascv" className="h-10 w-auto" />
        </button>

        {/* Stepper nav */}
        <nav className="flex items-end gap-8">
          {STEPS.map((step) => {
            const isActive = page === step.page
            const isDisabled = step.page === 'review' && !canReview

            return (
              <button
                key={step.page}
                type="button"
                disabled={isDisabled}
                onClick={() => onNavigate(step.page)}
                className="flex flex-col items-start disabled:cursor-not-allowed"
              >
                <span
                  className={`text-base ${
                    isDisabled ? 'text-brand/40' : 'text-brand'
                  }`}
                >
                  {step.num}
                </span>
                <span
                  className={`border-b-2 pb-0.5 text-xl ${
                    isActive
                      ? 'border-brand text-brand'
                      : isDisabled
                        ? 'border-transparent text-ink/40'
                        : 'border-transparent text-ink hover:text-brand'
                  }`}
                >
                  {step.label}
                </span>
              </button>
            )
          })}
        </nav>
      </div>
    </header>
  )
}

export default Header
