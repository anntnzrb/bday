from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

from .pipeline import process_file

USAGE = "Usage: bday [file]"


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])

    if len(args) != 1:
        print(USAGE, file=sys.stderr)
        return 1

    input_path = Path(args[0])
    process_file(input_path)
    return 0
