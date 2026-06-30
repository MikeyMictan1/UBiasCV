// ============================================================
// Footer
// Cream bar at the bottom of every page with the policy link.
// Link is a placeholder (href="#") until a real page exists.
// ============================================================

function Footer() {
  return (
    <footer className="border-t border-ink/30 bg-cream">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-10 py-4">
        <a href="#" className="text-base text-bodygray hover:text-brand">
          View our Framework and Policy on University AI Bias
        </a>
        <button type="button" className="text-base text-bodygray hover:text-brand">
          Privacy Policy
        </button>
      </div>
    </footer>
  )
}

export default Footer
