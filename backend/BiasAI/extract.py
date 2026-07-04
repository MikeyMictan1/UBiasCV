# Pull plain text out of an uploaded CV / feedback file.
# Supports the formats the frontend accepts: PDF, DOCX, TXT.

import io

import docx
import pypdf
from fastapi import UploadFile

MAX_FILE_BYTES = 2 * 1024 * 1024  # 2 MB per uploaded file
# Vercel's serverless functions hard-reject the whole request at 4.5MB (a
# platform limit, enforced before this code runs — see FUNCTION_PAYLOAD_TOO_LARGE).
# Two files at MAX_FILE_BYTES each stays safely under that with room for the
# multipart overhead and form fields.
MAX_TEXT_CHARS = 50_000  # ~12k tokens; well beyond any real CV or feedback doc


class FileTooLargeError(ValueError):
    """Raised when an uploaded file, or the text extracted from it, is too large."""


def extract_text(upload: UploadFile) -> str:
    raw = upload.file.read()
    if len(raw) > MAX_FILE_BYTES:
        raise FileTooLargeError(
            f"{upload.filename or 'File'} is too large "
            f"(max {MAX_FILE_BYTES // (1024 * 1024)}MB)."
        )

    name = (upload.filename or "").lower()

    if name.endswith(".pdf"):
        reader = pypdf.PdfReader(io.BytesIO(raw))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif name.endswith(".docx"):
        document = docx.Document(io.BytesIO(raw))
        text = "\n".join(p.text for p in document.paragraphs)
    else:
        # .txt and anything else: best-effort decode
        text = raw.decode("utf-8", errors="ignore")

    if len(text) > MAX_TEXT_CHARS:
        raise FileTooLargeError(
            f"{upload.filename or 'File'} contains too much text "
            f"(max {MAX_TEXT_CHARS:,} characters)."
        )

    return text
