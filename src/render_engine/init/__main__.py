import json
import sys
from argparse import ArgumentParser, ArgumentTypeError
from dataclasses import fields
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.prompt import Confirm, Prompt

from render_engine.init import InitOptions, create_site

console = Console(soft_wrap=True)
error_console = Console(stderr=True, soft_wrap=True)


def ask(answers: dict[str, Any], name: str, question: str) -> None:
    """Ask one question until the answer is valid, and store the answer in `answers`."""
    default = getattr(InitOptions(**answers), name)
    while True:
        if isinstance(default, bool):
            answers[name] = Confirm.ask(question, default=default, console=console)
        else:
            answers[name] = Prompt.ask(question, default=default, console=console)
        try:
            InitOptions(**answers)
            return
        except ValueError as error:
            console.print(str(error), style="red", markup=False)


def ask_options(defaults: dict[str, Any], destination: Path) -> InitOptions:
    """Ask the questions for a new site and return the answers."""
    answers = dict(defaults)
    ask(answers, "site_title", "Site title")
    ask(answers, "site_url", "Site URL")
    while True:
        ask(answers, "project_slug", "Project folder name")
        site_path = destination / InitOptions(**answers).project_slug
        if not site_path.exists():
            break
        console.print(
            f"The folder {str(site_path)!r} already exists. Please choose a different name.", style="red", markup=False
        )
    ask(answers, "app_filename", "App file name")
    ask(answers, "site_variable", "Name of the Site variable in the app file")
    ask(answers, "output_path", "Folder for the built site")
    ask(answers, "include_collection", "Include an example collection?")
    ask(answers, "include_blog", "Include an example blog?")
    ask(answers, "include_cli", "Use the Render Engine CLI?")
    return InitOptions(**answers)


def extra_context(text: str) -> dict[str, Any]:
    """Read the answers given with `--extra-context`, a JSON object like '{"site_title": "My Blog"}'."""
    try:
        answers = json.loads(text)
    except json.JSONDecodeError as error:
        raise ArgumentTypeError(f"not valid JSON ({error})") from None
    if not isinstance(answers, dict):
        raise ArgumentTypeError("""must be a JSON object, e.g. '{"site_title": "My Blog"}'""")

    known = [field.name for field in fields(InitOptions)]
    unknown = sorted(answers.keys() - set(known))
    if unknown:
        raise ArgumentTypeError(f"unknown answers {', '.join(unknown)}. The answers are: {', '.join(known)}")

    try:
        InitOptions(**answers)
    except (TypeError, ValueError) as error:
        raise ArgumentTypeError(str(error)) from None
    return answers


def destination_folder(text: str) -> Path:
    """Read `--output-dir`: the folder to create the project in. It's created if it doesn't exist."""
    path = Path(text)
    if path.exists() and not path.is_dir():
        raise ArgumentTypeError(f"{text!r} is a file, not a folder")
    return path


def main(argv: list[str] | None = None, prog: str = "render-engine-init") -> None:
    """Create a new Render Engine site from the command line.

    Asks the questions for the new site, or uses the default answers with `--no-input`,
    and creates the project folder inside the destination folder.
    """
    parser = ArgumentParser(
        prog=prog,
        description="Create a new Render Engine site.",
        epilog="Custom templates (--template) are no longer supported.",
    )
    parser.add_argument(
        "-e",
        "--extra-context",
        type=extra_context,
        default={},
        metavar="JSON",
        help="""Answers to use as defaults, as a JSON object, e.g. '{"site_title": "My Blog"}'.""",
    )
    parser.add_argument(
        "--no-input",
        action="store_true",
        help="Do not prompt for parameters.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=destination_folder,
        metavar="PATH",
        dest="destination",
        default=Path("."),
        help="Path to the folder in which to create the new project folder (default: the current folder).",
    )
    args = parser.parse_args(argv)

    try:
        if args.no_input:
            options = InitOptions(**args.extra_context)
        else:
            options = ask_options(args.extra_context, args.destination)
        site_path = create_site(options, args.destination)
    except KeyboardInterrupt:
        error_console.print("\nCancelled. No site was created.", style="yellow")
        sys.exit(130)
    except EOFError:
        error_console.print("\nThe input ended before all questions were answered. No site was created.", style="red")
        sys.exit(1)
    except (OSError, ValueError) as error:
        error_console.print(f"Couldn't create the site: {error}", style="red", markup=False)
        sys.exit(1)

    console.print(f"Created your new site in {site_path}", style="green", markup=False)
    console.print("Open its README.md to see how to build and preview it.")


if __name__ == "__main__":
    main()
