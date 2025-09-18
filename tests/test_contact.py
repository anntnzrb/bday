from __future__ import annotations

import pytest

from bday import contact


@pytest.mark.parametrize(
    "email,expected",
    [
        ("john.doe@example.com", True),
        ("user.name+tag@domain.co", True),
        ("invalid@domain", False),
        ("missing_at_symbol.com", False),
    ],
)
def test_is_valid_email(email: str, expected: bool) -> None:
    assert contact.is_valid_email(email) is expected


def test_extract_first_name_handles_commas_and_casing() -> None:
    assert contact.extract_first_name("Diaz, MARIA Fernanda") == "Maria"


def test_try_parse_contact_returns_struct() -> None:
    result = contact.try_parse_contact("Doe, John;;john.doe@example.com", ";")
    assert result == contact.Contact(name="John", email="john.doe@example.com")


@pytest.mark.parametrize(
    "line",
    [
        "",
        "Doe;;not-an-email",
        "OnlyTwoFields;john.doe@example.com",
    ],
)
def test_try_parse_contact_filters_invalid_rows(line: str) -> None:
    assert contact.try_parse_contact(line, ";") is None


def test_extract_first_name_empty_string_is_blank() -> None:
    assert contact.extract_first_name("   ") == ""
