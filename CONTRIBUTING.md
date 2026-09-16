# Contributing to SiteProbe

Thank you for your interest in contributing to SiteProbe!

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/tmolavi/siteprobe.git
   cd siteprobe
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install package in editable mode with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```bash
   pytest -v
   ```

## Adding New Checks

1. Create a new check class in `src/siteprobe/checks/<category>/` inheriting from `BaseCheck`.
2. Implement `run(page, all_pages, context) -> List[Finding]`.
3. Register the check in `src/siteprobe/checks/__init__.py`.
4. Add corresponding unit tests in `tests/test_checks.py`.

## Pull Request Guidelines
- Follow PEP 8 and run `ruff check .` before submitting.
- Ensure all tests pass with `pytest`.
- Provide meaningful commit messages and explain any breaking changes.
