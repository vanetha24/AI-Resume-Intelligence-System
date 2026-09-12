from pathlib import Path

import pymupdf
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF resume.
    """

    document = pymupdf.open(file_path)

    pages = []

    for page in document:
        page_text = page.get_text("text")

        if page_text:
            pages.append(page_text)

    document.close()

    return "\n".join(pages)


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX resume.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_resume_text(file_path: str) -> str:
    """
    Detect the resume format and extract its text.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":

        return extract_text_from_pdf(file_path)

    elif extension == ".docx":

        return extract_text_from_docx(file_path)

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please upload a PDF or DOCX resume."
        )