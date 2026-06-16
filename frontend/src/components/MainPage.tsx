// ============================================================
// MainPage
// Landing page of the toolkit:
//   1. CV / personal statement upload
//   2. AI feedback PDF upload
//   3. Context questionnaire (three dropdowns)
// "Generate Bias Report" just navigates to the results page for
// now — no backend connection yet.
// ============================================================

import { useState } from 'react'
import FileUpload from './FileUpload'

interface MainPageProps {
  onGenerate: () => void
}

// ---------- Questionnaire options ----------
const AI_TOOLS = ['ChatGPT', 'Claude', 'Gemini', 'Copilot', 'Other']
const COURSES = [
  'Liberal Arts',
  'Computer Science',
  'Engineering',
  'Medicine',
  'Law',
  'Business',
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
  // Questionnaire answers (kept here, ready to send to a backend later)
  const [aiTool, setAiTool] = useState(AI_TOOLS[0])
  const [course, setCourse] = useState(COURSES[0])
  const [gendered, setGendered] = useState(GENDERED_OPTIONS[0])

  return (
    <main className="mx-auto flex max-w-4xl flex-col items-center px-6 pb-20">
      {/* ---------- Steps 1 & 2: file uploads ---------- */}
      <div className="mt-4 flex flex-wrap justify-center gap-24">
        <FileUpload step={1} label="Input a CV/Personal Statement" />
        <FileUpload step={2} label="Input the AI tools Feedback PDF" />
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
            question="Which AI tool generated this feedback?"
            options={AI_TOOLS}
            value={aiTool}
            onChange={setAiTool}
          />
          <Dropdown
            question="What course is being applied for?"
            options={COURSES}
            value={course}
            onChange={setCourse}
          />
          <Dropdown
            question="Does the document contain any gendered identifiers?"
            options={GENDERED_OPTIONS}
            value={gendered}
            onChange={setGendered}
          />
        </div>
      </div>

      {/* ---------- Submit ---------- */}
      <button
        type="button"
        onClick={onGenerate}
        className="mt-10 rounded-md bg-[#4555B5] px-10 py-3 text-2xl font-bold text-white hover:bg-[#3F51A5]"
      >
        Generate Bias Report
      </button>
    </main>
  )
}

export default MainPage
