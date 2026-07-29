"""
importer.py

Knowledge Base Import Service

Responsibilities
----------------
- Import knowledge base ZIP
- Restore FAISS index
- Restore metadata
"""

from pathlib import Path
import zipfile
import shutil


class ImportService:

    DATABASE_FOLDER = Path("database")

    def import_zip(self, uploaded_file):
        """
        Restore a knowledge base from a ZIP archive.
        """

        # Ensure database folder exists
        self.DATABASE_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        # Remove existing contents
        for item in self.DATABASE_FOLDER.iterdir():

            if item.is_dir():
                shutil.rmtree(item)

            else:
                item.unlink()

        # Save uploaded ZIP temporarily
        temp_zip = self.DATABASE_FOLDER / "temp_import.zip"

        with open(temp_zip, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # Extract ZIP
        with zipfile.ZipFile(temp_zip, "r") as zip_file:
            zip_file.extractall(self.DATABASE_FOLDER)

        # Remove temporary ZIP
        temp_zip.unlink()

        return True