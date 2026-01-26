---
title: Testing, Linting, Formatting, and TypeChecking Render Engine
description: "The testing, linting, formatting, and typechecking steps including uv and justfiles"
date: Jan 25, 2026
---

Render engine uses `pytest` along with some other tools to ensure that render engine works as expected.

## Calling PyTest

The pytest dependencies are in a dependency group called `dev`. This allows us to call those dependencies in testing via `uv`.

You can call pytest via `uv` or the `justfile`.

### Using just

```bash
just test
```

### Using uv

```bash
`uv run --dev pytest tests`
```

## Tools that don't need to be installed

The tools required for Linting and Formatting (`ruff`) as well as type-checking (`mypy`) are not listed in the dependency group because they don't require other tools to be installed.

These tools can be called via `just`. If you wanted to run them without `just` you can use `uvx`

### Linting and Formatting

#### Using just for linting and formatting

```bash
just lint
```

```bash
just lint-fix
```

```bash
just format
```

To run the lint and format together:

```bash
just ruff
```

#### Using uvx for linting and formatting

```bash
uvx ruff format . # you can include --fix
uvx ruff check .
```

### Type Checking

#### Using just for type checking

```bash
just mypy
```

#### Using uvx for type checking

```bash
uvx mypy src
```
