// ============================================================
// Header
// Blue banner shown at the top of every page. The title changes
// per page ("University Admissions Bias Toolkit" / "Bias Report").
// The angled shapes are done with simple CSS clip-paths.
// ============================================================

interface HeaderProps {
  title: string
}

function Header({ title }: HeaderProps) {
  return (
    <header className="relative h-40 w-full overflow-hidden">
      {/* Base (lighter blue) layer */}
      <div
        className="absolute inset-0 bg-[#5C6BC0]"
        style={{ clipPath: 'polygon(0 0, 100% 0, 100% 100%, 50% 78%, 0 100%)' }}
      />

      {/* Darker blue diagonal band */}
      <div
        className="absolute inset-0 bg-[#3F51A5]"
        style={{ clipPath: 'polygon(0 55%, 100% 30%, 100% 82%, 50% 62%, 0 82%)' }}
      />

      {/* Page title */}
      <h1 className="relative z-10 pt-8 text-center text-4xl font-bold text-white">
        {title}
      </h1>
    </header>
  )
}

export default Header
