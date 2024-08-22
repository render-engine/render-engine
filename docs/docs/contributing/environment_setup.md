---
title: "Developing Locally"
description: "This document guides you through setting up a local development environment using Python, virtual environments, VS Code, Codespaces, and Dev Containers."
date: August 22, 2024
tags: ["setup", "python", "virtual-environment", "vs-code", "codespaces", "dev-containers"]
---

### Install Python

To develop locally you will need to have Python installed. Make sure you're using `Python 3.10.5` or higher to develop.

Visit <https://python.org> to learn more about installing Python.

### Create a Virtual Environment

Keep your default environment clean by installing a virtual environment.

```sh
python -m venv .venv
```

Once your virtual environment is created, you can activate it and install the requirements.

```sh
source .venv/bin/activate
python -m pip install --update pip
python -m pip install requirements.txt
```

  ![creating an virtual environment](https://vhs.charm.sh/vhs-5t8wsdubdq46vrJydWEtOi.gif)

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
