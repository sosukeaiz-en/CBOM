from typing import List
from app.models.schemas import RawFinding


def extract_context_window(file_content: str, line_number: int, window_size: int = 3) -> str:
    lines = file_content.splitlines()
    if not lines or line_number < 1 or line_number > len(lines):
        return ""
    start = max(0, line_number - 1 - window_size)
    end = min(len(lines), line_number + window_size)
    return "\n".join(lines[start:end])
