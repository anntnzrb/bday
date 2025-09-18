# bday

Transforms birthday contact spreadsheets into `name;email` CSVs.

The command accepts either `*.csv` or `*.xlsx` inputs and writes
`<input>.parsed.csv` alongside the source file.

> Legacy `*.xls` spreadsheets are not supported. Convert them to `.xlsx` or
> `.csv` before running the tool.

## Project layout
- `pyproject.toml`: project metadata and entry point (`bday.cli:main`).
- `src/bday/`: packaged application code using uv's recommended `src` layout.
- `tests/`: pytest suite covering contact parsing, pipeline, and CLI glue.
- `uv.lock`: lockfile maintained by `uv`.
