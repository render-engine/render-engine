# justfile for render-engine
# Requires: just, uv

# Default recipe to display available commands
default:
    @just --list

# Sync dependencies using uv
sync:
    uv sync --dev

# Run pytest with coverage
test FLAGS='':
    uv run --dev pytest {{FLAGS}}

# Run pytest with XML coverage report (for badge generation)
test-cov-report REPORT='xml':
    uv run --dev pytest --cov-report={{REPORT}}

# Run all nox sessions
nox:
    uvx nox

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
