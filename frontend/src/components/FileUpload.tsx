// ============================================================
// FileUpload
// Reusable upload box: numbered step badge + label, and a grey
// click-to-browse area. No backend yet — the chosen file name is
// just displayed so the user can see the selection worked.
// ============================================================

import { useRef, useState } from 'react'

interface FileUploadProps {
  step: number
  label: string
}

function FileUpload({ step, label }: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [fileName, setFileName] = useState<string | null>(null)

  return (
    <div className="flex flex-col items-start">
      {/* Step badge + label */}
      <div className="mb-2 flex items-center gap-2">
        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-[#3F51A5] text-sm font-bold text-white">
          {step}
        </span>
        <span className="text-sm font-medium text-gray-800">{label}</span>
      </div>

      {/* Clickable upload area */}
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        className="flex h-44 w-56 flex-col items-center justify-center rounded-md border border-gray-400 bg-gray-300 hover:bg-gray-200"
      >
        {/* Download-tray icon */}
        <svg
          className="h-12 w-12 text-gray-900"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M4 16v3a1 1 0 001 1h14a1 1 0 001-1v-3M12 4v11m0 0l-4-4m4 4l4-4"
          />
        </svg>

        {/* Selected file name, or accepted-formats hint */}
        {fileName ? (
          <span className="mt-3 max-w-[13rem] truncate px-2 text-xs font-medium text-gray-800">
            {fileName}
          </span>
        ) : (
          <span className="mt-3 text-[10px] font-semibold text-gray-700">
            Accepted: PDF, DOCX, TXT
          </span>
        )}
      </button>

      {/* Hidden native file input */}
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx,.txt"
        className="hidden"
        onChange={(e) => setFileName(e.target.files?.[0]?.name ?? null)}
      />
    </div>
  )
}

export default FileUpload
