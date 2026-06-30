// ============================================================
// FileUpload
// Dashed "Drop or Browse" zone used inside the Input Data cards.
// Supports click-to-browse and drag-and-drop; once a file is
// chosen its name replaces the "Drop or Browse" label.
// ============================================================

import { useRef, useState } from 'react'

interface FileUploadProps {
  // Reports the chosen file (or null) up to the parent
  onFileSelect: (file: File | null) => void
}

function FileUpload({ onFileSelect }: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [fileName, setFileName] = useState<string | null>(null)

  function selectFile(file: File | null) {
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
        className="flex w-full flex-col items-center justify-center border-2 border-dashed border-ink/30 px-4 py-12 text-center hover:border-brand"
      >
        {/* Download-tray icon */}
        <svg
          className="h-12 w-12 text-ink"
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

        <span className="mt-3 max-w-full truncate px-2 text-2xl text-ink">
          {fileName ?? 'Drop or Browse'}
        </span>
        <span className="mt-2 text-sm tracking-wider text-bodygray">
          PDF | DOCX | TXT
        </span>
      </button>

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
