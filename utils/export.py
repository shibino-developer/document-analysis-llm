"""
export.py

Knowledge Base Export Service

Responsibilities
----------------
- Export FAISS index
- Export metadata
- Create ZIP archive
"""

from pathlib import Path
import zipfile


class ExportService:

    KNOWLEDGE_BASE_FOLDER = Path("database/knowledge_base")

    EXPORTS_FOLDER = Path("exports")

    EXPORT_NAME = "knowledge_base.zip"

    def export(self) -> Path:
        """
        Export the knowledge base as a ZIP archive.
        """

        self.EXPORTS_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        export_path = (
            self.EXPORTS_FOLDER /
            self.EXPORT_NAME
        )

        with zipfile.ZipFile(
            export_path,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            for file in self.KNOWLEDGE_BASE_FOLDER.rglob("*"):

                if file.is_file():

                    zip_file.write(
                        file,
                        arcname=file.relative_to(
                            self.KNOWLEDGE_BASE_FOLDER
                        )
                    )

        return export_path