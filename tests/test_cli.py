from __future__ import annotations

from pathlib import Path
import runpy

import pytest

from bday import cli


def test_main_requires_single_argument(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = cli.main([])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Usage: bday [file]" in captured.err


def test_main_invocation_creates_output(tmp_path: Path) -> None:
    csv = tmp_path / "input.csv"
    csv.write_text(
        "name;middle;email\nDoe, John;;john.doe@example.com\n",
        encoding="utf-8",
    )

    exit_code = cli.main([str(csv)])

    assert exit_code == 0
    assert (tmp_path / "input.parsed.csv").read_text(encoding="utf-8") == (
        "name;email\nJohn;john.doe@example.com\n"
    )


def test_package_entrypoint(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {}

    def fake_main(argv: list[str] | None = None) -> int:
        called["value"] = argv
        return 0

    monkeypatch.setattr("bday.cli.main", fake_main)

    with pytest.raises(SystemExit) as exc:
        runpy.run_module("bday", run_name="__main__")

    assert exc.value.code == 0
    assert called["value"] is None
