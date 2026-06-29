// ============================================================
// Footer
// Fixed bar at the bottom of every page with policy links.
// Links are placeholders (href="#") until real pages exist.
// ============================================================

function Footer() {
  return (
    <footer className="fixed bottom-0 left-0 z-20 flex w-full items-center justify-between bg-[#5C6BC0] px-4 py-2">
      <a href="#" className="text-sm font-bold text-purple-900 hover:underline">
        View our Framework and AI Gender Bias Policy Here
      </a>
      <a href="#" className="text-sm font-bold text-purple-900 hover:underline">
        Privacy Policy
      </a>
    </footer>
  )
}

export default Footer
