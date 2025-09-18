from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pytest

from bday import io


def test_stringify_value_branches() -> None:
    assert io._stringify_value(None) == ""
    assert io._stringify_value("text") == "text"
    assert io._stringify_value(date(2025, 1, 2)) == "2025-01-02"
    assert io._stringify_value(datetime(2025, 1, 2, 3, 4, 5)) == "2025-01-02T03:04:05"
    assert io._stringify_value(3.0) == "3"
    assert io._stringify_value(3.14) == "3.14"
    assert io._stringify_value({"k": 1}) == "{'k': 1}"


def test_read_excel_lines_rejects_xls(tmp_path: Path) -> None:
    legacy = tmp_path / "contacts.xls"
    legacy.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Legacy .xls files are not supported"):
        io.read_excel_lines(legacy)


def test_read_excel_lines_with_invalid_extension(tmp_path: Path) -> None:
    bogus = tmp_path / "contacts.ods"
    bogus.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        io.read_excel_lines(bogus)
