import os
import pathlib

import nox

VENV_DIR = pathlib.Path("./.venv").resolve()
PYTHON_VERSIONS = ["3.13", "3.12", "3.11", "3.10"]


@nox.session
def develop(session: nox.Session, python="3.12") -> None:
    """Setup your developer environment"""
    session.install("virtualenv")
    session.run("virtualenv", os.fsdecode(VENV_DIR), silent=True)
    python = os.fsdecode(VENV_DIR.joinpath("bin/python"))

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensures it's installed in the right way
    session.run(python, "-m", "pip", "install", "-e", ".[dev]", external=True)


@nox.session
def lint(session, python="3.12"):
    """Lint using ruff"""

    session.install("ruff")
    session.run("ruff", "check", "--fix", ".")
    session.run("ruff", "format", ".")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run the test suite"""
    session.run("pytest", "tests")
