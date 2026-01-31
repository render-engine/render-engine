---
title: GitHub Actions File Patterns
description: "How to use file patterns in GitHub Actions to optimize CI runs"
---

File patterns in GitHub Actions allow you to run workflows only when specific files change. This helps optimize CI
usage by preventing unnecessary test runs when irrelevant files are modified.

## Why Use File Patterns?

GitHub Actions provides free CI minutes, but they are limited. By using file patterns, you can:

- **Save CI minutes** - Only run tests when code changes, not for documentation updates
- **Faster feedback** - Skip irrelevant workflows to get results faster
- **Better resource usage** - Reduce unnecessary compute usage

## Basic Syntax

Use the `paths` filter in your workflow to specify which file changes should trigger the workflow:

```yaml
on:
  pull_request:
    paths:
      - "src/**"
      - "tests/**"
      - "pyproject.toml"
```

This workflow will only run when files in `src/`, `tests/`, or `pyproject.toml` are modified.

## Pattern Matching

GitHub Actions uses glob patterns for file matching:

- `*` - Matches zero or more characters (except `/`)
- `**` - Matches zero or more directories
- `?` - Matches a single character
- `[abc]` - Matches any character in the brackets
- `[!abc]` - Matches any character NOT in the brackets

### Examples

| Pattern     | Matches                                                        |
| ----------- | -------------------------------------------------------------- |
| `*.py`      | All Python files in the root directory                         |
| `**/*.py`   | All Python files in any directory                              |
| `src/**`    | All files in the `src` directory and subdirectories            |
| `*.{py,md}` | All Python and Markdown files in the root directory            |
| `!docs/**`  | Exclude all files in the `docs` directory                      |

## Render Engine Examples

### Test Workflow

The test workflow only runs when code-related files change:

```yaml
name: PyTest
on:
  pull_request:
    paths:
      - ".github/workflows/test.yml"
      - "src/**"
      - "tests/**"
      - "pyproject.toml"
      - "requirements.txt"
```

This prevents test runs when only documentation files are modified.

### Excluding Patterns

Use `paths-ignore` to exclude specific files:

```yaml
on:
  pull_request:
    paths-ignore:
      - "docs/**"
      - "**/*.md"
      - "*.txt"
```

This workflow will run for all changes except those in the `docs/` directory, Markdown files, or text files.

> **NOTE**
> You cannot use both `paths` and `paths-ignore` in the same workflow. Choose the approach that makes your intent
> clearer.

## Best Practices

### 1. Include Workflow File Changes

Always include the workflow file itself in the paths filter. This ensures the workflow runs when you modify it:

```yaml
on:
  pull_request:
    paths:
      - ".github/workflows/test.yml"  # Include the workflow file
      - "src/**"
      - "tests/**"
```

### 2. Include Dependency Files

Include files that affect dependencies or build configuration:

```yaml
on:
  pull_request:
    paths:
      - "pyproject.toml"     # Python dependencies
      - "requirements.txt"   # Pip requirements
      - "uv.lock"            # UV lock file
      - "src/**"
```

### 3. Use Specific Patterns

Be specific with your patterns to avoid missing important changes:

```yaml
# Good ✓ - Specific paths
paths:
  - "src/render_engine/**/*.py"
  - "tests/**/*.py"

# Avoid ✗ - Too broad
paths:
  - "**"
```

### 4. Document Your Patterns

Add comments to explain why specific paths are included:

```yaml
on:
  pull_request:
    paths:
      # Workflow configuration
      - ".github/workflows/test.yml"
      # Source code
      - "src/**"
      # Test files
      - "tests/**"
      # Dependencies
      - "pyproject.toml"
```

### 5. Consider Cross-Cutting Concerns

Some files affect multiple areas of your project. Include them when relevant:

```yaml
on:
  pull_request:
    paths:
      - "src/**"
      - "tests/**"
      - "pyproject.toml"      # Dependencies affect all code
      - ".github/workflows/**" # Workflow changes need validation
```

## Testing Your Patterns

### Local Testing

You can test if files match your patterns using `git diff` with the `--name-only` flag:

```bash
# Get list of changed files in your branch
git diff --name-only main...your-branch

# Test if files match a pattern
git diff --name-only main...your-branch | grep "src/"
```

### GitHub Actions Context

GitHub provides the `github.event.pull_request.changed_files` context in workflows, but pattern matching happens
automatically before the workflow runs.

## Common Patterns in Render Engine

Here are the file patterns used across Render Engine workflows:

### Code Tests

```yaml
paths:
  - ".github/workflows/test.yml"
  - "src/**"
  - "tests/**"
  - "pyproject.toml"
  - "requirements.txt"
```

### Documentation Labels

From `.github/labeler.yml`:

```yaml
documentation:
  - changed-files:
    - any-glob-to-any-file: ['docs/**', 'guides/**']
    - any-glob-to-any-file: '**/*.md'
```

### Source Code Labels

```yaml
source:
  - all:
    - changed-files:
      - any-glob-to-any-file: 'src/**/*'
      - all-globs-to-all-files: '!src/docs/*'
```

## Troubleshooting

### Workflow Not Running When Expected

If your workflow doesn't run when you expect it to:

1. **Check the file paths** - Ensure the changed files match your patterns
2. **Verify glob syntax** - Test patterns locally with `find` or `ls`
3. **Review exclusions** - Make sure you're not excluding files unintentionally
4. **Check branch filters** - Ensure the workflow runs on the correct branch

### Workflow Running Too Often

If your workflow runs more often than expected:

1. **Narrow your patterns** - Use more specific paths
2. **Use paths-ignore** - Exclude files that should not trigger runs
3. **Add conditional jobs** - Use `if` conditions within jobs for finer control

## Additional Resources

- [GitHub Actions: Workflow syntax for paths](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore)
- [GitHub Actions: Filter pattern cheat sheet](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet)
- [GitHub Actions Labeler](https://github.com/actions/labeler) - For automatic PR labeling based on file patterns
