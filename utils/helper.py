import os


SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".txt"]


def get_file_extension(filename: str):
    return os.path.splitext(filename)[1].lower()


def is_supported_file(filename: str):
    return get_file_extension(filename) in SUPPORTED_EXTENSIONS