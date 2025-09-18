# bday

Python CLI that transforms birthday contact spreadsheets into `name;email` CSVs.

## Usage
```bash
uv run bday <input-file>
```

The command accepts either `*.csv` or `*.xlsx` inputs and writes
`<input>.parsed.csv` alongside the source file.

> Legacy `*.xls` spreadsheets are not supported. Convert them to `.xlsx` or
> `.csv` before running the tool.
