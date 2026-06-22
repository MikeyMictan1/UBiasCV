# Pull plain text out of an uploaded CV / feedback file.
# Supports the formats the frontend accepts: PDF, DOCX, TXT.

import io

import docx
import pypdf
from fastapi import UploadFile


def extract_text(upload: UploadFile) -> str:
    raw = upload.file.read()
    name = (upload.filename or "").lower()

    if name.endswith(".pdf"):
        reader = pypdf.PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if name.endswith(".docx"):
        document = docx.Document(io.BytesIO(raw))
        return "\n".join(p.text for p in document.paragraphs)

    # .txt and anything else: best-effort decode
    return raw.decode("utf-8", errors="ignore")

# import fitz (Potential Better Alternative)

# def extract_text(upload: UploadFile) -> str:
#     raw = upload.file.read()
#     name = (upload.filename or "").lower()

#     if name.endswith(".pdf"):
#         doc = fitz.open(stream=raw, filetype="pdf")
#         try:
#             parts = []
#             for page_num, page in enumerate(doc):
#                 text = page.get_text()
#                 parts.append(text)
#                 parts.append(f"\n\n--- Page {page_num + 1} ---\n\n")
#             return "".join(parts)
#         finally:
#             doc.close()

#     if name.endswith(".docx"):
#         document = docx.Document(io.BytesIO(raw))
#         return "\n".join(p.text for p in document.paragraphs)

#     return raw.decode("utf-8", errors="ignore")