from pathlib import Path
from pypdf import PdfReader
from docx import Document

from utils.helper import is_supported_file


class DocumentLoader:

    def __init__(self):
        pass

    def load_document(self, uploaded_file):

        if uploaded_file is None:
            raise Exception("No file uploaded.")

        if not is_supported_file(uploaded_file.name):
            raise Exception("Unsupported file type.")

        suffix = Path(uploaded_file.name).suffix.lower()

        if suffix == ".pdf":
            return self._load_pdf(uploaded_file)

        elif suffix == ".docx":
            return self._load_docx(uploaded_file)

        elif suffix == ".txt":
            return self._load_txt(uploaded_file)

    def _load_pdf(self, uploaded_file):

        pdf = PdfReader(uploaded_file)

        text = ""

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return {
            "filename": uploaded_file.name,
            "filetype": "PDF",
            "pages": len(pdf.pages),
            "text": text
        }

    def _load_docx(self, uploaded_file):

        doc = Document(uploaded_file)

        paragraphs = []

        for para in doc.paragraphs:
            paragraphs.append(para.text)

        text = "\n".join(paragraphs)

        return {
            "filename": uploaded_file.name,
            "filetype": "DOCX",
            "paragraphs": len(doc.paragraphs),
            "text": text
        }

    def _load_txt(self, uploaded_file):

        text = uploaded_file.read().decode("utf-8")

        return {
            "filename": uploaded_file.name,
            "filetype": "TXT",
            "lines": len(text.splitlines()),
            "text": text
        }