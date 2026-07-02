// ============================================================
// InputDataPage
// Page 02. Two file-upload cards (CV + AI feedback) and a Context
// card with three dropdowns, then "Generate Bias Report". On
// submit it posts everything to /api/analyze and, on success,
// hands the report up to App (which shows the Review page).
// ============================================================

import { useState } from 'react'
import FileUpload from './FileUpload'
import type { BiasReport } from '../types'

interface InputDataPageProps {
  user: string
  // Called with the generated report once the backend responds
  onReport: (report: BiasReport) => void
}

// ---------- Questionnaire options ----------
const AI_TOOLS = [
  'VMock',
  'ChatGPT',
  'Claude',
  'Gemini',
  'Copilot',
  'Other',
]
const COURSES = [
  'Art',
  'History',
  'Liberal Arts',
  'Computer Science',
  'Engineering',
  'Medicine',
  'Law',
  'Business',
  'Psychology',
  'Sociology',
  'Economics',
  'Political Science',
  'Philosophy',
  'Mathematics',
  'Physics',
  'Chemistry',
  'Biology',
  'Education',
  'Other',
]
const GENDERED_OPTIONS = ['Yes', 'No', 'Unsure', 'Prefer not to say']

const PLACEHOLDER = '- SELECT -'

// ---------- Card scaffold (numbered header + body) ----------
interface CardProps {
  num: string
  title: string
  children: React.ReactNode
}

function Card({ num, title, children }: CardProps) {
  return (
    <div className="border border-ink/20">
      <div className="flex items-baseline gap-3 border-b border-ink/20 bg-cream px-5 py-3">
        <span className="text-xl font-bold text-brand">{num}</span>
        <span className="text-xl text-bodygray">{title}</span>
      </div>
      <div className="bg-white p-6">{children}</div>
    </div>
  )
}

// ---------- Labelled dropdown ----------
interface FieldProps {
  label: string
  options: string[]
  value: string
  onChange: (value: string) => void
  helper?: string
}

function Field({ label, options, value, onChange, helper }: FieldProps) {
  return (
    <div className="flex flex-col">
      <label className="mb-2 text-sm tracking-wider text-bodygray">{label}</label>
      {helper && <p className="mb-2 text-sm text-bodygray">{helper}</p>}
      <div className="relative">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full appearance-none border border-ink/30 bg-white px-3 py-2 pr-10 text-ink focus:border-brand focus:outline-none"
        >
          <option value="">{PLACEHOLDER}</option>
          {options.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
        <svg
          className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-brand"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M6 9l6 6 6-6" />
        </svg>
      </div>
    </div>
  )
}

function InputDataPage({ user, onReport }: InputDataPageProps) {
  const [cvFile, setCvFile] = useState<File | null>(null)
  const [feedbackFile, setFeedbackFile] = useState<File | null>(null)
  const [aiTool, setAiTool] = useState('')
  const [course, setCourse] = useState('')
  const [gendered, setGendered] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleGenerate() {
    if (!cvFile || !feedbackFile) {
      setError('Please upload both a CV and the AI feedback file.')
      return
    }
    setError(null)
    setLoading(true)

    const form = new FormData()
    form.append('cv', cvFile)
    form.append('ai_feedback', feedbackFile)
    form.append('user', user)
    form.append('ai_tool', aiTool)
    form.append('course', course)
    form.append('gendered', gendered)

    try {
      const res = await fetch('/api/analyze', { method: 'POST', body: form })
      if (!res.ok) {
        const body = await res.json().catch(() => null)
        const detail = body?.detail
        // FastAPI sends a string for HTTPExceptions (400/502) but an array of
        // {loc, msg} objects for 422 validation errors — handle both.
        const message = Array.isArray(detail)
          ? detail.map((e) => `${e.loc?.slice(1).join('.')}: ${e.msg}`).join('; ')
          : typeof detail === 'string'
            ? detail
            : `Request failed (${res.status})`
        throw new Error(message)
      }
      const report = await res.json()
      onReport(report)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto w-full max-w-6xl px-10 py-8">
      <p className="mb-6 text-base text-brand">Input Data</p>

      {/* Uploads */}
      <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
        <Card num="01" title="The CV">
          <FileUpload onFileSelect={setCvFile} />
        </Card>
        <Card num="02" title="AI Tool Feedback">
          <FileUpload onFileSelect={setFeedbackFile} />
        </Card>
      </div>

      {/* Context */}
      <div className="mt-8">
        <Card num="03" title="Context">
          <p className="mb-5 text-sm text-bodygray">
            These details help tailor the analysis and the recommendations that
            follow.
          </p>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            <Field
              label="AI TOOL USED"
              options={AI_TOOLS}
              value={aiTool}
              onChange={setAiTool}
            />
            <Field
              label="AREA OF WORK/STUDY"
              options={COURSES}
              value={course}
              onChange={setCourse}
            />
            <Field
              label="GENDERED IDENTIFIERS OR LANGUAGE?"
              options={GENDERED_OPTIONS}
              value={gendered}
              onChange={setGendered}
            // helper="Optional. Use this to flag whether the CV includes gender-coded wording or identifiers." Research says this is a sensitive question and that we should make it a netral option with an explicit helper line?
            />
          </div>

        </Card>
      </div>

      {/* Submit */}
      <button
        type="button"
        onClick={handleGenerate}
        disabled={loading}
        className="mt-8 flex items-center gap-3 bg-brand px-8 py-4 text-2xl font-bold text-white hover:bg-[#16466f] active:bg-[#103a5d] disabled:opacity-70"
      >
        {loading ? (
          <>
            <span className="h-6 w-6 animate-spin rounded-full border-[3px] border-white/40 border-t-white" />
            Generating...
          </>
        ) : (
          'Generate Bias Report →'
        )}
      </button>

      {error && <p className="mt-4 text-base font-medium text-coral">{error}</p>}
    </div>
  )
}

export default InputDataPage
