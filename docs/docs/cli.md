---
title: "Render Engine CLI"
description: "Guide to using Render Engine CLI for creating, building, and serving your site."
date: August 22, 2024
tags: ["render-engine", "cli", "site-setup", "build", "serve"]
---

Render Engine comes with a CLI that can be used to create, build, and serve your site.

## pyproject.toml Configuration

The Render Engine CLI can be configured through your `pyproject.toml` file to set default values and avoid repetitive command-line arguments.

### Configuration Structure

```toml
[render-engine.cli]
module = "your_module"
site = "YourSiteClass"
collection = "blog"  # optional
```

### Configuration Options

- **module**: The Python module containing your Site class
- **site**: The name of your Site class within the module
- **collection**: Default collection name for the `new-entry` command

### Example Configuration

```toml
[render-engine.cli]
module = "my_site"
site = "MySite"
collection = "posts"
```

With this configuration, commands that normally require `module:site` can be run without arguments:

- `render-engine build` instead of `render-engine build my_site:MySite`
- `render-engine serve` instead of `render-engine serve my_site:MySite`

## CLI Commands

### init

Create a new Render Engine site from a template.

```bash
render-engine init [TEMPLATE] [OPTIONS]
```

**Arguments:**

- `TEMPLATE`: Template URL or path (default: <https://github.com/render-engine/cookiecutter-render-engine-site>)

**Options:**

- `--extra-context, -e`: Extra context as JSON string
- `--no-input`: Skip all prompts
- `--output-dir`: Output directory (default: ./)
- `--config-file, -c`: Path to cookiecutter config file

**Examples:**

```bash
# Use default template
render-engine init

# Use custom template with no prompts
render-engine init https://github.com/myuser/mytemplate --no-input

# Provide extra context
render-engine init --extra-context '{"project_name": "My Blog"}'
```

### build

Build your static site.

```bash
render-engine build [MODULE:SITE] [OPTIONS]
```

**Arguments:**

- `MODULE:SITE`: Module path and site class (e.g., `my_site:MySite`)

**Options:**

- `--clean, -c`: Remove output folder before building

**Examples:**

```bash
# Basic build
render-engine build my_site:MySite

# Build with clean
render-engine build my_site:MySite --clean

# Using config defaults
render-engine build
```

### serve

Serve your site locally with auto-reload capability.

```bash
render-engine serve [MODULE:SITE] [OPTIONS]
```

**Arguments:**

- `MODULE:SITE`: Module path and site class

**Options:**

- `--clean, -c`: Clean output folder before building
- `--reload, -r`: Auto-reload on file changes
- `--directory, -d`: Directory to serve (default: output)
- `--port, -p`: Port number (default: 8000)

**Examples:**

```bash
# Basic serve
render-engine serve my_site:MySite

# Serve with auto-reload on port 3000
render-engine serve my_site:MySite --reload --port 3000

# Clean build and serve
render-engine serve my_site:MySite --clean --reload
```

### templates

List available templates from installed themes.

```bash
render-engine templates [MODULE:SITE] [OPTIONS]
```

**Arguments:**

- `MODULE:SITE`: Module path and site class

**Options:**

- `--theme-name`: Specific theme to list templates from
- `--filter-value`: Filter templates by name

**Examples:**

```bash
# List all templates
render-engine templates my_site:MySite

# List templates from specific theme
render-engine templates my_site:MySite --theme-name bootstrap

# Filter templates containing "post"
render-engine templates my_site:MySite --filter-value post
```

### new-entry

Create a new collection entry (blog post, page, etc.).

```bash
render-engine new-entry [MODULE:SITE] [COLLECTION] [FILENAME] [OPTIONS]
```

**Arguments:**

- `MODULE:SITE`: Module path and site class
- `COLLECTION`: Collection name (e.g., "blog", "pages")
- `FILENAME`: Output filename for the new entry

**Options:**

- `--content`: Content string for the entry
- `--content-file`: Path to file containing content
- `--title`: Entry title
- `--slug`: URL slug for the entry
- `--args`: Additional metadata as key=value or key:value pairs
- `--include-date`: Add today's date to the entry. NOTE: If this is set and a
date is included in the `--args` the one from the `--args` will be used.

**Examples:**

```bash
# Create a basic blog post
render-engine new-entry my_site:MySite blog my-first-post.md --title "My First Post"

# Create post with content
render-engine new-entry my_site:MySite blog hello.md --content "Hello, world!" --title "Hello"

# Create post from file with metadata
render-engine new-entry my_site:MySite blog review.md \
    --content-file draft.txt \
    --title "Product Review" \
    --args author="John Doe" \
    --args category=reviews \
    --args tags="product,tech"

# Using slug
render-engine new-entry my_site:MySite pages about.md \
    --title "About Us" \
    --slug "about-us"

# With --include-date
render-engine new-entry my_site:MySite pages about.md \
    --include-date
```

**Notes:**

- The `--args` option can be used multiple times
- Arguments can use either `=` or `:` as separator
- If `EDITOR` environment variable is set, the file opens automatically after creation
- Cannot use both `--content` and `--content-file` options

## Usage Tips

1. **Configuration First**: Set up your `pyproject.toml` to avoid typing module:site repeatedly
2. **Development Workflow**: Use `serve --reload` during development for instant feedback
3. **Clean Builds**: Use `--clean` flag when switching between major changes
4. **Template Discovery**: Use `templates --filter-value` to find specific template types
5. **Batch Entry Creation**: Combine `new-entry` with shell scripts for bulk content creation
