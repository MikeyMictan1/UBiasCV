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
      className="flex w-full flex-col gap-2 px-4 py-4 text-left hover:bg-beige/70 sm:flex-row sm:items-center sm:justify-between sm:gap-4 sm:px-6 sm:py-5"
    >
      <span>
        <span className="block text-xl font-bold text-brand sm:text-2xl">{title}</span>
        <span className="block text-sm text-bodygray sm:text-base">{subtitle}</span>
      </span>
      <span className="text-lg font-bold text-brand sm:text-2xl">Select →</span>
    </button>
  )
}

function IntroPage({ onSelectUser }: IntroPageProps) {
  return (
    <div className="py-6 sm:py-8">
      <div className="mx-auto w-full max-w-6xl px-4 sm:px-6 lg:px-10">
        <p className="mb-3 text-base text-brand">Introduction</p>

        <h1 className="mb-6 text-3xl font-bold text-brand sm:text-4xl">
          Detecting Gender Bias in AI CV Feedback Tools
        </h1>
        <p className="max-w-4xl text-base text-ink sm:text-lg">
          UBiasCV compares a CV against AI-generated feedback, and detects gender
          bias introduced by the AI with a score, flagged phrases, and next steps.
        </p>
      </div>

      {/* Full-bleed logo banner */}
      <div className="my-6 flex items-center justify-center bg-brand py-6 sm:my-8 sm:py-10">
        <img src={logoHero} alt="ubiascv" className="h-16 w-auto sm:h-28" />
      </div>

      <div className="mx-auto w-full max-w-6xl px-4 sm:px-6 lg:px-10">
        <h2 className="mb-5 text-2xl font-bold text-brand sm:text-3xl">Who Is Using The Tool?</h2>

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
