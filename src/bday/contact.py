from __future__ import annotations

from dataclasses import dataclass
import re


EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


@dataclass(frozen=True)
class Contact:
    name: str
    email: str


def is_valid_email(email: str) -> bool:
    """Return True when email matches the expected pattern."""

    return bool(EMAIL_PATTERN.fullmatch(email))


def _first_token(text: str) -> str:
    tokens = text.strip().split()
    return tokens[0] if tokens else ""


def _capitalize(name: str) -> str:
    if not name:
        return ""

    lowered = name.lower()
    return f"{lowered[0].upper()}{lowered[1:]}"


def extract_first_name(full_name: str) -> str:
    """Replicate the F# extractFirstName behaviour."""

    parts = full_name.split(",", 1)
    candidate = parts[1] if len(parts) == 2 and parts[1].strip() else full_name
    return _capitalize(_first_token(candidate))


def try_parse_contact(line: str, delimiter: str) -> Contact | None:
    """Parse a semicolon-delimited line into a contact."""

    fields = line.split(delimiter, 2)
    if len(fields) != 3:
        return None

    name_raw, _, email = fields
    if not name_raw:
        return None

    if not is_valid_email(email):
        return None

    return Contact(name=extract_first_name(name_raw), email=email)
