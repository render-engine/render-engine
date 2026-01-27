---
title: "Developing Locally"
description: "This document guides you through setting up a local development environment using Python, virtual environments, VS Code, Codespaces, and Dev Containers."
date: August 22, 2024
tags: ["setup", "python", "virtual-environment", "vs-code", "codespaces", "dev-containers"]
---

### Python Version

To develop locally you will need to have Python installed. Make sure you're using `Python 3.10.5` or higher to develop.

Visit <https://python.org> to learn more about installing Python.

### Create a Virtual Environment

This project uses [uv](https://github.com/astral-sh/uv). It's highly recommended that you use 'uv' to manage your environment and use all tools included.

- install `uv` according to your [OS instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)

### Justfile

There are a series of commands saved in a [justfile](https://github.com/casey/just).

- install just using your [OS insctructions](https://github.com/casey/just?tab=readme-ov-file#installation)
- you can view the available commands with `just`

```text
Available recipes:
    badge                        # Generate coverage badge
    ci                           # Run full CI workflow (sync, lint, test, badge)
    default                      # Default recipe to display available commands
    format directory='.'         # Run ruff formatter as check
    format-fix directory='.'     # Run ruff formatter and fix issues
    lint directory='.'           # Run ruff linter without fixing
    lint-fix directory='.'       # Run ruff linter with auto-fix
    nox                          # Run all nox sessions
    pytest version *FLAGS=''     # Run tests in arbitrary Python version.
    ruff
    ruff-fix directory='.'       # Run both linter and formatter, fixing issues.
    sync                         # Sync dependencies using uv
    test *FLAGS=''               # Run pytest
    test-cov-report REPORT='xml' # Run pytest with coverage report (defaults to XML)
    ty PATH='src'                # Run ty type checker
```

#### Using VS Code

If you're using [Visual Studio Code](https://code.visualstudio.com/) you can also create a virtual environment from the command pallet. This will also enable the installation of the dependencies.

![Creating an Environment using VS Code](<../assets/create environment vs code.gif>)

## Using Codespaces

You can create a new codespace to quickly get started with your project.

You can create a codespace on main.

![Create a Codespace](../assets/create-codespace.gif)

This will create a codespace in which you can make your changes. Don't worry they won't let you push your changes directly to the codebase but when you go to make that change it will let you create a fork and submit the PR.

There is a `devcontainer.json` designed to give you a good start on developing for Render Engine, including getting extensions and settings.

## Using Dev Containers

If you don't want to use Codespaces you can still use the pre-configured environment in VS Code using a Dev Container.

To use dev containers, you will need to have VS Code installed, Docker, and the dev Container extension.

Start with ensuring that the docker daemon is running.

Open your fork of the project in VS Code and open the command pallet. Next, Enter "Dev Containers: ReOpen in Container" and select the option.

This will create a new local environment with the same configuration as the [codespace](#using-codespaces).

![Launching a Dev Container](<../assets/launching a dev container.gif>)
