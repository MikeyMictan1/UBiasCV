// ============================================================
// MainPage
// Landing page of the toolkit:
//   1. CV upload
//   2. AI feedback PDF upload
//   3. Context questionnaire (three dropdowns)
// "Generate Bias Report" just navigates to the results page for
// now — no backend connection yet.
// ============================================================

import { useState } from 'react'
import FileUpload from './FileUpload'
import type { BiasReport } from '../types'

interface MainPageProps {
  // Called with the generated report once the backend responds
  onGenerate: (report: BiasReport) => void
}

// ---------- Questionnaire options ----------
const AI_TOOLS = ['VMock', 'ChatGPT', 'Claude', 'Gemini', 'Copilot', 'Other']
const USER = ['Student', 'Tool Developer']
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
const GENDERED_OPTIONS = ['- Select -', 'Yes', 'No', 'Unsure']

// Small helper for a labelled dropdown row (bullet + question + select)
interface DropdownProps {
  question: string
  options: string[]
  value: string
  onChange: (value: string) => void
}

function Dropdown({ question, options, value, onChange }: DropdownProps) {
  return (
    <div className="flex flex-col items-start">
      <div className="mb-1 flex items-center gap-2">
        <span className="h-2.5 w-2.5 rounded-full bg-[#3F51A5]" />
        <label className="text-sm text-gray-800">{question}</label>
      </div>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-72 rounded-sm border border-gray-400 bg-gray-200 px-2 py-1.5 text-sm text-gray-800"
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  )
}

function MainPage({ onGenerate }: MainPageProps) {
  // Questionnaire answers
  const [user, setUser] = useState(USER[0])
  const [aiTool, setAiTool] = useState(AI_TOOLS[0])
  const [course, setCourse] = useState(COURSES[0])
  const [gendered, setGendered] = useState(GENDERED_OPTIONS[0])

  // Uploaded files + request state
  const [cvFile, setCvFile] = useState<File | null>(null)
  const [feedbackFile, setFeedbackFile] = useState<File | null>(null)
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
        const detail = await res.json().catch(() => null)
        throw new Error(detail?.detail ?? `Request failed (${res.status})`)
      }
      const report = await res.json()
      onGenerate(report)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="mx-auto flex max-w-4xl flex-col items-center px-6 pb-20">
      {/* ---------- Steps 1 & 2: file uploads ---------- */}
      <div className="mt-4 flex flex-wrap justify-center gap-24">
        <FileUpload
          step={1}
          label="Input a CV"
          onFileSelect={setCvFile}
        />
        <FileUpload
          step={2}
          label="Input the AI tools Feedback"
          onFileSelect={setFeedbackFile}
        />
      </div>

      {/* ---------- Step 3: questionnaire ---------- */}
      <div className="mt-10 flex flex-col items-start">
        <div className="mb-4 flex items-center gap-2">
          <span className="flex h-7 w-7 items-center justify-center rounded-full bg-[#3F51A5] text-sm font-bold text-white">
            3
          </span>
          <span className="text-sm font-medium text-gray-800">
            Potential questionnaire/dropdown options to give extra context
          </span>
        </div>

        <div className="flex flex-col gap-4 pl-9">
        <Dropdown
            question="Who is using this tool?"
            options={USER}
            value={user}
            onChange={setUser}
          />
          <Dropdown
            question="Which AI tool generated this feedback?"
            options={AI_TOOLS}
            value={aiTool}
            onChange={setAiTool}
          />
          <Dropdown
            question="What area of study/work is the CV intended for?"
            options={COURSES}
            value={course}
            onChange={setCourse}
          />
          <Dropdown
            question="Does the CV contain any gendered identifiers?"
            options={GENDERED_OPTIONS}
            value={gendered}
            onChange={setGendered}
          />
        </div>
      </div>

      {/* ---------- Submit ---------- */}
      <button
        type="button"
        onClick={handleGenerate}
        disabled={loading}
        className="mt-10 rounded-md bg-[#4555B5] px-10 py-3 text-2xl font-bold text-white hover:bg-[#3F51A5] disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? 'Analyzing…' : 'Generate Bias Report'}
      </button>

      {error && <p className="mt-4 text-sm font-medium text-red-700">{error}</p>}
    </main>
  )
}

export default MainPage
