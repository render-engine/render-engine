---
title: Style Guide
description: "Guidelines for formatting content"
---

This guide documents both automated formatting rules (enforced by linters) and manual style preferences for the Render Engine project.

## Automated Formatting

### Ruff (Python)

Render Engine uses [Ruff](https://docs.astral.sh/ruff/) for Python linting and formatting with the following configuration:

- **Line length**: 120 characters
- **Indent width**: 4 spaces
- **Target version**: Python 3.10+
- **Rules enabled**: E (pycodestyle errors), F (Pyflakes), I (isort), UP (pyupgrade)

Ruff automatically formats imports, fixes common errors, and enforces PEP 8 style guidelines.

### Markdown

Markdown files are linted using markdownlint with configuration in `.markdownlint.json`.

- **Line length**: 120 characters maximum

## Python Style Preferences

### Function and Method Signatures

When a function or method has multiple parameters, prefer placing each parameter on its own line for better readability:

```python
# Preferred ✓
def create_entry(
    self,
    filepath: Path = None,
    editor: str = None,
    content: str = None,
    metadata: dict = None,
) -> str:
    """Create a new entry for the Collection."""
    pass

# Avoid ✗
def create_entry(self, filepath: Path = None, editor: str = None, content: str = None, metadata: dict = None) -> str:
    """Create a new entry for the Collection."""
    pass
```

For simple functions with one or two parameters, single-line signatures are acceptable:

```python
# Acceptable for simple signatures
def get_title(self) -> str:
    """Return the title."""
    return self._title

def process(self, value: str) -> None:
    """Process the given value."""
    pass
```

### Type Hint Ordering

Use modern Python union syntax (`|`) instead of `Union` from typing. Order types with specific types first, and `None` last:

```python
# Preferred ✓
def get_page(
    self,
    content_path: str | Path | None = None,
) -> Page:
    pass

# Also acceptable
template: str | None
routes: list[str | Path]

# Avoid ✗ - Old Union syntax
from typing import Union, Optional

def get_page(
    self,
    content_path: Union[str, Path, None] = None,
) -> Page:
    pass

# Avoid ✗ - None in the middle
content_path: str | None | Path
```

### Type Annotations

Always include type hints for function parameters and return values:

```python
# Preferred ✓
def process_content(
    self,
    content: str,
    max_length: int = 100,
    strict: bool = False,
) -> str:
    """Process content with type hints for all parameters."""
    pass

def get_pages(self, count: int) -> list[Page]:
    """Return pages with typed parameters."""
    return self._pages[:count]

# Avoid ✗ - Missing type hints
def process_content(self, content, max_length=100, strict=False):
    """Process content without type hints."""
    pass
```

## Justfile Style

Just is a command-shortcutting tool used to simplify calling commands.

### Comment and Indentation

Justfile commands should have a `#`-led comment that explains the command above the command definition.

The command body must be indented 4 spaces:

```just
# Preferred ✓
# Sync dependencies using uv
sync:
    uv sync --dev

# Run tests with coverage report (defaults to XML)
test-cov-report REPORT='xml':
    uv run --dev pytest --cov-report={{ REPORT }}
```

### Parameter Naming

Parameters should be in `UPPER` casing. When used in the command, wrap the parameter in double braces with a space
between the inner braces and the parameter name:

```just
# Preferred ✓
# Run ruff linter without fixing
lint DIRECTORY='.':
    uvx ruff check {{ DIRECTORY }}

# Avoid ✗ - lowercase parameters or no spaces in braces
lint directory='.':
    uvx ruff check {{directory}}
```

### Command Organization

Group related commands together and use consistent naming patterns:

```just
# Preferred ✓
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
    uvx ruff format {{ DIRECTORY }}
```
