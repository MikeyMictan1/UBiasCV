// ============================================================
// FileUpload
// Dashed "Drop or Browse" zone used inside the Input Data cards.
// Supports click-to-browse and drag-and-drop; once a file is
// chosen its name replaces the "Drop or Browse" label.
// ============================================================

import { useRef, useState } from 'react'

// Must match backend/BiasAI/extract.py MAX_FILE_BYTES. Vercel's serverless
// functions hard-reject the whole request at 4.5MB before our code ever
// runs, so we check client-side and fail fast instead of letting the user
// wait through a slow upload that's doomed anyway.
const MAX_FILE_BYTES = 2 * 1024 * 1024 // 2 MB

function formatSize(bytes: number): string {
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`
}

interface FileUploadProps {
  // Reports the chosen file (or null) up to the parent
  onFileSelect: (file: File | null) => void
}

function FileUpload({ onFileSelect }: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [fileName, setFileName] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  function selectFile(file: File | null) {
    if (file && file.size > MAX_FILE_BYTES) {
      setError(`${file.name} is ${formatSize(file.size)} — max size is ${formatSize(MAX_FILE_BYTES)}.`)
      setFileName(null)
      onFileSelect(null)
      return
    }
    setError(null)
    setFileName(file?.name ?? null)
    onFileSelect(file)
  }

  return (
    <>
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault()
          selectFile(e.dataTransfer.files?.[0] ?? null)
        }}
        className="flex w-full flex-col items-center justify-center border-2 border-dashed border-ink/30 px-4 py-8 text-center hover:border-brand sm:py-12"
      >
        {/* Download-tray icon */}
        <svg
          className="h-10 w-10 text-ink sm:h-12 sm:w-12"
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

        <span className="mt-3 max-w-full truncate px-2 text-xl text-ink sm:text-2xl">
          {fileName ?? 'Drop or Browse'}
        </span>
        <span className="mt-2 text-sm tracking-wider text-bodygray">
          PDF | DOCX | TXT — max {formatSize(MAX_FILE_BYTES)}
        </span>
      </button>

      {error && <p className="mt-2 text-sm font-medium text-coral">{error}</p>}

      {/* Hidden native file input */}
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx,.txt"
        className="hidden"
        onChange={(e) => selectFile(e.target.files?.[0] ?? null)}
      />
    </>
  )
}

export default FileUpload
