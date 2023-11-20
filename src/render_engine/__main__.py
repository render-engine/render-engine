"""Enables the use of `python -m render_engine` to run the CLI."""

from .cli.cli import app

if __name__ == "__main__":
    app()
