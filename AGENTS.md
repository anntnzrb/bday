# AGENTS.md

## Project Structure & Module Organization
- Application code lives in `src/bday/`. Key modules: `cli.py` (entrypoint), `pipeline.py` (orchestration), `io.py` (file access), and `contact.py` (data shaping).
- Tests mirror the package layout under `tests/`, using `test_*.py` files to cover CLI, pipeline, I/O, and parsing.
- Root assets include `pyproject.toml` for dependency metadata, `uv.lock` for reproducible installs, and this guide. Generated outputs (e.g., `*.parsed.csv`) must stay out of version control.

## Build, Test, and Development Commands
- `uv sync` – install runtime and dev dependencies into the project-managed virtual environment.
- `uv run bday <input.csv>` – execute the CLI against a CSV (or `.xlsx`) source to produce `<input>.parsed.csv`.
- `uv run pytest` – run the full test suite.
- `uv run pytest --cov=bday --cov-report=term-missing` – execute tests with line coverage details.

## Coding Style & Naming Conventions
- Keep modules small and focused; shared helpers belong in `contact.py` or a new module under `src/bday/`.
- Prefer `pathlib.Path`, explicit encodings, and f-strings.

## Testing Guidelines
- Pytest is the required framework; locate tests next to the feature area they cover (`test_pipeline.py`, etc.).
- Name tests `test_<behavior>` for clarity and keep assertions specific.
- Maintain 100 % line coverage (`--cov=bday`) when adding or modifying code. Add regression cases whenever you introduce new error handling or edge paths.

## Security & Configuration Notes
- Never commit real contact data or credentials. Use anonymized fixtures under `tests/`.
- Let `uv` manage virtual environments locally.
