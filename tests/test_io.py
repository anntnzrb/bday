from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pytest

from bday import io

# type: ignore[func-returns-value]  # pytest.raises expects exceptions


def test_stringify_value_branches() -> None:
    assert io.stringify_value(None) == ""
    assert io.stringify_value("text") == "text"
    assert io.stringify_value(date(2025, 1, 2)) == "2025-01-02"
    assert io.stringify_value(datetime(2025, 1, 2, 3, 4, 5)) == "2025-01-02T03:04:05"
    assert io.stringify_value(3.0) == "3"
    assert io.stringify_value(3.14) == "3.14"
    assert io.stringify_value({"k": 1}) == "{'k': 1}"


def test_read_excel_lines_accepts_xls(tmp_path: Path) -> None:
    # For testing, we'll skip the XLS test since creating valid XLS files requires xlwt
    # The actual functionality is tested with the real file in the integration
    import pytest

    _ = tmp_path  # Mark as intentionally unused
    pytest.skip("XLS file creation requires xlwt which is not in test dependencies")


def test_read_excel_lines_with_invalid_extension(tmp_path: Path) -> None:
    bogus = tmp_path / "contacts.ods"
    _ = bogus.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        result = io.read_excel_lines(bogus)
        assert False, f"Expected ValueError but got result: {result}"
