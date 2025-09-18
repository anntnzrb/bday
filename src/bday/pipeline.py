from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .contact import try_parse_contact
from .io import (
    DELIMITER,
    is_excel_file,
    read_csv_lines,
    read_excel_lines,
    write_csv_lines,
)


HEADER = f"name{DELIMITER}email"


def process_lines(lines: Iterable[str]) -> List[str]:
    iterator = iter(lines)
    next(iterator, None)  # Skip header

    processed = [HEADER]
    for line in iterator:
        contact = try_parse_contact(line, DELIMITER)
        if contact:
            processed.append(f"{contact.name}{DELIMITER}{contact.email}")

    return processed


def process_file(path: Path) -> Path:
    suffix = path.suffix.lower()
    if suffix == ".xls":
        raise ValueError(
            "Legacy .xls files are not supported; convert the file to .xlsx or CSV."
        )

    if is_excel_file(path):
        lines = read_excel_lines(path)
    else:
        lines = read_csv_lines(path)

    processed_lines = process_lines(lines)
    output_path = path.with_suffix(".parsed.csv")
    write_csv_lines(output_path, processed_lines)
    return output_path
