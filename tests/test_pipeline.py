from __future__ import annotations

from pathlib import Path

import openpyxl
import pytest

from bday.pipeline import process_file, process_lines


def test_process_lines_filters_and_formats() -> None:
    rows = [
        "name;middle;email",
        "Doe, John;;john.doe@example.com",
        "Doe, Jane;;invalid",
    ]

    result = process_lines(rows)

    assert result == [
        "name;email",
        "John;john.doe@example.com",
    ]


def test_process_file_with_csv(tmp_path: Path) -> None:
    csv = tmp_path / "contacts.csv"
    csv.write_text(
        "name;middle;email\nDoe, John;;john.doe@example.com\n;;invalid\n",
        encoding="utf-8",
    )

    output = process_file(csv)

    assert (
        output.read_text(encoding="utf-8") == "name;email\nJohn;john.doe@example.com\n"
    )


def test_process_file_with_xlsx(tmp_path: Path) -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["name", "middle", "email"])
    sheet.append(["Doe, John", "", "john.doe@example.com"])
    sheet.append(["", "", "invalid"])

    xlsx_path = tmp_path / "contacts.xlsx"
    workbook.save(xlsx_path)

    output = process_file(xlsx_path)
    assert (
        output.read_text(encoding="utf-8") == "name;email\nJohn;john.doe@example.com\n"
    )


def test_process_file_rejects_xls(tmp_path: Path) -> None:
    xls_path = tmp_path / "contacts.xls"
    xls_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Legacy .xls files are not supported"):
        process_file(xls_path)
