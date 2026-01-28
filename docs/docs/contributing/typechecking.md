---
title: Typechecking
date: 27 Jan 2026
description: Defines how developers should type
---

## Type Checking with ty

This project uses [ty][ty] as its primary type checker. ty is included in the dev dependencies and
provides static type analysis for the codebase.

### Running ty

The easiest way to run ty is through the `justfile`:

```bash
just ty
```

This command runs `uv run ty check src` to check all source files. You can also specify a custom path:

```bash
just ty path/to/specific/file.py
```

Or run ty directly with uv:

```bash
uv run --dev ty check src
```

Note: Currently, ty checking does not fail the build due to existing issues that are being resolved incrementally.

## Type Hint Ordering Policy

When writing optional types, always place the primary type **before** `None`.

### Preferred ✓

```python
def get_site_map(self) -> SiteMap | None:
    return self._site_map

def process_template(template: str | Template | None = None) -> str:
    ...

static_dir: str | pathlib.Path | None = None
```

### Not Preferred ✗

```python
def get_site_map(self) -> None | SiteMap:  # Wrong order
    return self._site_map

def process_template(template: None | str | Template = None) -> str:  # Wrong order
    ...
```

[ty]: https://github.com/astral-sh/ty
