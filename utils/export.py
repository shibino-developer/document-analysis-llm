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

    DATABASE_FOLDER = Path("database")

    EXPORT_NAME = "knowledge_base.zip"

    def export(self) -> Path:
        """
        Export the knowledge base as a ZIP archive.
        """

        export_path = self.DATABASE_FOLDER / self.EXPORT_NAME

        with zipfile.ZipFile(
            export_path,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            for file in self.DATABASE_FOLDER.rglob("*"):

                if (
                    file.is_file()
                    and file.name != self.EXPORT_NAME
                ):

                    zip_file.write(
                        file,
                        arcname=file.relative_to(
                            self.DATABASE_FOLDER
                        )
                    )

        return export_path