// ============================================================
// Footer
// Cream bar at the bottom of every page with the policy link.
// The framework link is a placeholder (href="#") until a real page
// exists; Privacy Policy navigates to the in-app PrivacyPolicyPage.
// ============================================================

import type { PageName } from '../App'

interface FooterProps {
  onNavigate: (page: PageName) => void
}

function Footer({ onNavigate }: FooterProps) {
  return (
    <footer className="border-t border-ink/30 bg-cream">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-2 px-4 py-4 text-center sm:flex-row sm:justify-between sm:gap-4 sm:px-6 sm:text-left lg:px-10">
        <a href="#" className="text-sm text-bodygray hover:text-brand sm:text-base">
          View our Framework and Policy on University AI Bias
        </a>
        <button
          type="button"
          onClick={() => onNavigate('privacy')}
          className="text-sm text-bodygray hover:text-brand sm:text-base"
        >
          Privacy Policy
        </button>
      </div>
    </footer>
  )
}

export default Footer
