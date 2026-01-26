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
test *FLAGS='': (pytest DEFAULT_PYTHON_VERSION FLAGS)

# Run tests in arbitrary Python version.
pytest version *FLAGS='':
    uv run -p {{version}} --dev pytest {{FLAGS}}

# Run pytest with coverage report (defaults to XML)
test-cov-report REPORT='xml':
    uv run --dev pytest --cov-report={{REPORT}}

# Run all nox sessions
nox:
    uvx nox

# Run ruff linter without fixing
lint directory='.':
    uvx ruff check {{ directory }}

# Run ruff linter with auto-fix
lint-fix directory='.':
    uvx ruff check --fix {{ directory }}

# Run ruff formatter as check
format directory='.':
    uvx ruff format --check {{ directory }}

# Run ruff formatter and fix issues
format-fix directory='.':
    uvx ruff format --check {{ directory }}

ruff: lint format

# Run both linter and formatter, fixing issues.
ruff-fix directory='.':
    @# Prefacing with `-` to ignore any errors that might be fixed by formatting.
    -uvx ruff check --fix {{ directory }}
    uvx ruff format {{ directory }}
    uvx ruff check {{ directory }}
    @echo "\nEverything looks good!"

# Run mypy type checker
mypy:
    -uvx mypy src # For the moment we have way too many issues in mypy so not having it fail.

# Generate coverage badge
badge: (test '--cov-report=xml')
    uvx --with "genbadge[coverage]" genbadge coverage -i coverage.xml

# Run full CI workflow (sync, lint, test, badge)
ci: sync nox ruff mypy badge
