# justfile for render-engine
# Requires: just, uv

# Default recipe to display available commands
default:
    @just --list

# Sync dependencies using uv
sync:
    uv sync --extra dev

# Run pytest with coverage
test:
    uv run --extra dev pytest

# Run pytest with verbose output
test-v:
    uv run --extra dev pytest -v

# Run pytest with coverage report
test-cov:
    uv run --extra dev pytest --cov-report=term-missing

# Run pytest with XML coverage report (for badge generation)
test-cov-report REPORT='xml':
    uv run --extra dev pytest --cov-report={{REPORT}}

# Run all nox sessions
nox:
    uv run nox

# Run nox test sessions for all Python versions
nox-test:
    uv run nox -s test

# Run ruff linter
lint:
    uvx ruff check .

# Run ruff linter with auto-fix
lint-fix:
    uvx ruff check --fix .

# Run ruff formatter
format:
    uvx ruff format .

# Run both linter and formatter
ruff: lint-fix format

# Run mypy type checker
mypy:
    uvx mypy src

# Generate coverage badge
badge:
    uv run --extra dev pytest --cov-report=xml
    uvx --with "genbadge[coverage]" genbadge coverage -i coverage.xml

# Run full CI workflow (sync, lint, test, badge)
ci: sync nox ruff mypy test badge
