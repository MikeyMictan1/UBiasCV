// ============================================================
// PrivacyPolicyPage
// Plain-language explanation of hosting, data handling, and the
// Claude API call. Reached via the Footer's "Privacy Policy" link.
// ============================================================

interface PrivacyPolicyPageProps {
  onBack: () => void
}

interface SectionProps {
  title: string
  children: React.ReactNode
}

function Section({ title, children }: SectionProps) {
  return (
    <section className="mb-8 sm:mb-10">
      <h2 className="mb-2 text-xl font-bold text-brand sm:text-2xl">{title}</h2>
      <div className="mt-1 mb-4 border-b border-ink/25" />
      <div className="space-y-3 text-base text-bodygray sm:text-lg">{children}</div>
    </section>
  )
}

function PrivacyPolicyPage({ onBack }: PrivacyPolicyPageProps) {
  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-6 sm:px-6 sm:py-8 lg:px-10">
      <button
        type="button"
        onClick={onBack}
        className="mb-4 text-sm text-brand hover:underline sm:text-base"
      >
        ← Back
      </button>

      <p className="mb-3 text-base text-brand">Privacy Policy</p>
      <h1 className="mb-6 text-3xl font-bold text-brand sm:text-4xl">
        How ubiascv handles your data
      </h1>
      <p className="mb-10 max-w-3xl text-base text-ink sm:text-lg">
        This page explains, in plain terms, what happens to your CV and AI
        feedback file when you use this tool, where the app is hosted, and
        what is (and isn't) tracked.
      </p>

      <Section title="Hosting">
        <p>
          ubiascv is hosted on <strong className="text-ink">Vercel</strong>. Vercel
          serves the frontend and runs the backend as serverless functions. We
          don't operate our own servers or databases — every request is
          handled by Vercel's infrastructure and nothing is written to a
          persistent store on our end.
        </p>
      </Section>

      <Section title="No analytics or tracking">
        <p>
          This tool does not use any analytics, advertising, or tracking
          scripts — no Google Analytics, no Vercel Analytics, no cookies, and
          no third-party trackers of any kind. We don't know who you are, and
          we don't collect usage statistics beyond what your browser and
          Vercel's own infrastructure logs generate to keep the service
          running (standard request logs, not tied to an account or profile).
        </p>
      </Section>

      <Section title="Your CV and feedback files">
        <p>
          When you upload a CV and AI feedback file, they're read into memory
          for the single request that generates your report, then discarded.
          Nothing is saved to a database or disk — there's no account, no
          history, and no way for us to retrieve a file you've previously
          uploaded, because it was never stored in the first place.
        </p>
      </Section>

      <Section title="The Claude API call">
        <p>
          Generating a report sends your CV text, the AI feedback text, and
          your questionnaire answers to Anthropic's Claude API in a single,
          one-off request to produce the analysis. Claude does not retain
          memory between requests — each report is generated fresh, with no
          access to any other user's data and no memory of your previous
          uploads, because there aren't any to remember.
        </p>
      </Section>

      <Section title="Questions">
        <p>
          If you have questions about this policy or how the tool works,
          reach out to the team behind the Responsible AI Consortium (RAIC)
          project.
        </p>
      </Section>
    </div>
  )
}

export default PrivacyPolicyPage
