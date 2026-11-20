---
title: "Installing Render Engine and Creating Your First Site"
description: "Instructions for installing Render Engine and, creating and testing your first site."
date: November 9, 2026
tags: ["installation", "render-engine", "initialization", "cli"]
---

To use Render Engine, you must have Python 3.11 or greater (supporting Python 3.11, 3.12, 3.13, 3.14, and 3.15)
installed. You can download Python from [python.org].

- Linux/MacOS: [python.org]
- Windows: Install Python using [pymanager on Microsoft Store][ms-store], which manages Python installations.

## Install Render Engine

Render Engine is available on PyPI:

```bash
pip install render-engine   # pip
uv add render-engine        # uv
```

This is all you need if you write your `app.py` yourself and build the site with `python app.py`.
To create a new site from a template and use commands like `render-engine serve`, install the CLI
as described in [Create your site](#create-your-site).

## Create your site

The easiest way to start is the `render-engine init` command from [render-engine-cli].
It creates a new folder with a ready-to-use site. Choose **one** of the options below.

### With `pip`

1. Create a virtual environment and activate it. This keeps your site's packages separate from
   other Python projects:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # on Windows: .venv\Scripts\activate
    ```

2. Install the CLI. It also installs Render Engine itself:

    ```bash
    pip install render-engine-cli
    ```

3. Create your site and move into the new folder. The folder is named after the site title you
   choose, for example "My Awesome Website":

    ```bash
    render-engine init
    cd my-awesome-website
    ```

4. Fix `pyproject.toml` as described in [Tell the CLI where your site is](#tell-the-cli-where-your-site-is).

### With uv

`uvx` runs the CLI once, so you don't need to install anything first:

```bash
uvx --from render-engine-cli render-engine init
cd my-awesome-website
```

Add the CLI to the project:

```bash
uv add --dev render-engine-cli
```

A dev dependency is enough, because your server only needs the generated HTML files, not the `render-engine` command line tool.

Finally, fix `pyproject.toml` as described in [Tell the CLI where your site is](#tell-the-cli-where-your-site-is).

### Answer the `init` questions

`render-engine init` asks a few questions. Press Enter to accept the default shown in brackets.

| Question | Default | What it does |
|---|---|---|
| What is the URL of your site | `http://example.com` | Your site's address, used in links, RSS feeds and the sitemap. You can change it later in `app.py`. |
| Output Directory Name | `output` | Folder where the built HTML files are written. |
| What is the name of the main app file | `app.py` | The Python file that defines your site. **Currently ignored:** the file is always created as `app.py`. |
| The title of your site | `Untitled Site` | Shown on your site's pages. |
| `project_slug` | based on the title | Name of the new folder for your site. |
| `skip_collection` | `n` | Answer `y` to create the site **without** an example collection of pages. |
| `skip_blog` | `n` | Answer `y` to create the site **without** a blog. |

> !!! NOTE
    `skip_collection` and `skip_blog` ask whether to **skip** a feature, so answer `n` (no)
    to keep it and `y` (yes) to leave it out.

### Tell the CLI where your site is

The generated `pyproject.toml` tells the CLI which file and object are your site. This can be very helpful as it removes the requirement of passing the `--module-site` parameter to many of the CLI commands. Rename the
`[render-engine.cli]` table to `[tool.render-engine.cli]` so the CLI can find it:

```toml
[tool.render-engine.cli]
module = "app"
site = "app"
collection = "blog"
```

If you chose a different app file name, set module to that name without .py.

### Run your site

```bash
render-engine serve         # pip (with the virtual environment activated)
uv run render-engine serve  # uv
```

Open the address shown in the terminal to see your site.

## Init options

`init` has a few options that you can use to customize your site.

You can view the options using the `--help` flag.

```text
$ render-engine init --help
Usage: render-engine init [OPTIONS]

  Create a new site configuration. You can provide extra_context to the
  cookiecutter template.

  Also, any argument that cookiecutter accepts can be passed to this command.

  The template can be a local path or a git repository.

Options:
  -e, --extra-context TEXT  Extra context to pass to the cookiecutter
                            template. This must be a JSON string.
  -t, --template TEXT       Template to use for creating a new site.
  --no-input                Do not prompt for parameters.
  -o, --output-dir PATH
  -c, --config-file PATH
  --help                    Show this message and exit.
```

Visit the [CLI - init] page for more information.

## Additional modules

Render Engine also supports multiple parsers and modules. You will need to install them separately.

For example, to use the RSS parser, install the [render-engine-rss] module:

```bash
pip install render-engine-rss   # or: uv add render-engine-rss
```

### Continue to [Simple Site Layout]

[cli - init]: ../cli/docs/cli.md
[simple site layout]: layout.md

[render-engine-cli]: https://pypi.org/project/render-engine-cli/
[render-engine-rss]: https://pypi.org/project/render-engine-rss/

[ms-store]: https://apps.microsoft.com/detail/9NQ7512CXL7T
[python.org]: https://python.org
