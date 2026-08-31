from io import BytesIO

from pypdf import PdfReader
from docx import Document


def extract_pdf_text(
    file_bytes: bytes,
):

    reader = PdfReader(
        BytesIO(file_bytes)
    )

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_docx_text(
    file_bytes: bytes,
):

    document = Document(
        BytesIO(file_bytes)
    )

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(
                paragraph.text
            )

    return "\n".join(paragraphs)