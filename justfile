# justfile for render-engine
# Requires: just, uv

# Default recipe to display available commands
default:
    @just --list

[doc('Sync dependencies using uv')]
sync:
    uv sync --extra dev

# Run pytest with coverage
test FLAGS='':
    uv run --extra dev pytest {{FLAGS}}:

# Run pytest with XML coverage report (for badge generation)
test-cov-report REPORT='xml':
    uv run --extra dev pytest --cov-report={{REPORT}}

# Run all nox sessions
nox:
    uvx run nox

# Run nox test sessions for all Python versions
nox-test:
    uvx run nox -s test

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
ruff: lint format

# Run mypy type checker
mypy:
    uvx mypy src

# Generate coverage badge
badge: test-cov-report
    uvx --with "genbadge[coverage]" genbadge coverage -i coverage.xml

# Run full CI workflow (sync, lint, test, badge)
ci: sync nox ruff mypy test badge
