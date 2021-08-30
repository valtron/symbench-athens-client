from pathlib import Path


def get_test_file_path(filename):
    return Path(__file__).resolve().parent / "files" / filename
