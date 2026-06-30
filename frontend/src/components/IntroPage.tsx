// ============================================================
// IntroPage
// Page 01. Explains the tool, shows the logo banner, and asks who
// is using it. Selecting a role records the user and advances to
// the Input Data page.
// ============================================================

import logoHero from '../assets/logo-hero.png'

interface IntroPageProps {
  // Called with the chosen role ("Student" | "Tool Developer")
  onSelectUser: (user: string) => void
}

interface RoleRowProps {
  title: string
  subtitle: string
  onSelect: () => void
}

function RoleRow({ title, subtitle, onSelect }: RoleRowProps) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className="flex w-full items-center justify-between px-6 py-5 text-left hover:bg-beige/70"
    >
      <span>
        <span className="block text-2xl font-bold text-brand">{title}</span>
        <span className="block text-base text-bodygray">{subtitle}</span>
      </span>
      <span className="text-2xl font-bold text-brand">Select →</span>
    </button>
  )
}

function IntroPage({ onSelectUser }: IntroPageProps) {
  return (
    <div className="py-8">
      <div className="mx-auto w-full max-w-6xl px-10">
        <p className="mb-3 text-base text-brand">Introduction</p>

        <h1 className="mb-6 text-4xl font-bold text-brand">
          Detecting Gender Bias in AI CV Feedback Tools
        </h1>
        <p className="max-w-4xl text-lg text-ink">
          ubiascv compares a CV against AI-generated feedback, and detects gender
          bias introduced by the AI with a score, flagged phrases, and next steps.
        </p>
      </div>

      {/* Full-bleed logo banner */}
      <div className="my-8 flex items-center justify-center bg-brand py-10">
        <img src={logoHero} alt="ubiascv" className="h-28 w-auto" />
      </div>

      <div className="mx-auto w-full max-w-6xl px-10">
        <h2 className="mb-5 text-3xl font-bold text-brand">Who Is Using The Tool?</h2>

        <div className="border border-ink/25 bg-white">
          <RoleRow
            title="Student"
            subtitle="I received AI CV feedback"
            onSelect={() => onSelectUser('Student')}
          />
          <div className="border-t border-ink/15" />
          <RoleRow
            title="Tool Developer"
            subtitle="I build an AI CV feedback tool"
            onSelect={() => onSelectUser('Tool Developer')}
          />
        </div>
      </div>
    </div>
  )
}

export default IntroPage
