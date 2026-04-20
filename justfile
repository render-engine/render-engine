# justfile for render-engine
# Requires: just, uv

DEFAULT_PYTHON_VERSION := "3.14"

# Default recipe to display available commands
default:
    @just --list

# Sync dependencies using uv
sync:
    uv sync --dev

# Run pytest
test *FLAGS='':
    pytest {{ DEFAULT_PYTHON_VERSION }} {{ FLAGS }}

# Run tests in arbitrary Python version.
pytest VERSION *FLAGS='':
    uv run -p {{ VERSION }} --dev pytest {{ FLAGS }}

# Run pytest with coverage report (defaults to XML)
test-cov-report REPORT='xml':
    uv run --dev pytest --cov-report={{ REPORT }}

# Run all nox sessions
nox:
    uvx nox

docs:
    @echo "Starting documentation server..."
    mkdocs serve -f docs/mkdocs.yml -a 0.0.0.0:8000

# Run markdown linter (requires bun or npm)
lint-md DIRECTORY=".":
    #!/usr/bin/env sh
    if command -v bun > /dev/null 2>&1; then
        bunx markdownlint-cli2 {{ DIRECTORY }}
    elif command -v npm > /dev/null 2>&1; then
        npx markdownlint-cli2 {{ DIRECTORY }}
    else
        echo "Error: neither bun nor npm found. Install one of them to run markdown linting." >&2
        exit 1
    fi

# Run ruff linter without fixing
lint DIRECTORY='.':
    uvx ruff check {{ DIRECTORY }}

# Run ruff linter with auto-fix
lint-fix DIRECTORY='.':
    uvx ruff check --fix {{ DIRECTORY }}

# Run ruff formatter as check
format DIRECTORY='.':
    uvx ruff format --check {{ DIRECTORY }}

# Run ruff formatter and fix issues
format-fix DIRECTORY='.':
    uvx ruff format --check {{ DIRECTORY }}

ruff: lint format

# Run both linter and formatter, fixing issues.
ruff-fix DIRECTORY='.':
    @# Prefacing with `-` to ignore any errors that might be fixed by formatting.
    -uvx ruff check --fix {{ DIRECTORY }}
    uvx ruff format {{ DIRECTORY }}
    uvx ruff check {{ DIRECTORY }}
    @echo "\nEverything looks good!"

# Run ty type checker
ty PATH='src':
    uv run ty check {{ PATH }} # For the moment we have way too many issues in ty so not having it fail.

# Generate coverage badge
badge: (test-cov-report 'xml')
    uvx --with "genbadge[coverage]" genbadge coverage -i coverage.xml

# Run full CI workflow (sync, lint, test, badge)
ci: sync nox ruff ty badge
