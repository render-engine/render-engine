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


def ask(answers: dict[str, Any], name: str, question: str) -> Any:
    """Ask one question until the answer is valid, and return the answer.

    :param answers: The answers so far, used for the default and to check the new answer.
    :param name: The name of the answer, e.g. `site_title`.
    :param question: The question shown to the user.
    :return: The valid answer: text, or True/False for yes/no questions.
    """
    default = getattr(InitOptions(**answers), name)
    while True:
        if isinstance(default, bool):
            answer = Confirm.ask(question, default=default, console=console)
        else:
            answer = Prompt.ask(question, default=default, console=console)
        new_answers: dict[str, Any] = {**answers, name: answer}
        try:
            InitOptions(**new_answers)
            return answer
        except ValueError as error:
            console.print(str(error), style="red", markup=False)


def ask_project_folder(answers: dict[str, Any], destination: Path) -> tuple[str, Path]:
    """Ask for the project folder name, and return it with the path of the new site.

    :param answers: The answers so far.
    :param destination: The folder the project folder will be created in.
    :return: The typed folder name, and the path of the new site.
    """
    project_slug = ask(answers, "project_slug", "Project folder name")
    new_answers: dict[str, Any] = {**answers, "project_slug": project_slug}
    site_path = destination / InitOptions(**new_answers).project_slug

    return project_slug, site_path


def ask_options(defaults: dict[str, Any], destination: Path) -> InitOptions:
    """Ask the questions for a new site and return the answers.

    :param defaults: Answers to use as defaults, from `--extra-context`.
    :param destination: The folder the project folder will be created in.
    :return: The answers.
    """
    answers = dict(defaults)
    answers["site_title"] = ask(answers, "site_title", "Site title")
    answers["site_url"] = ask(answers, "site_url", "Site URL")
    answers["project_slug"], site_path = ask_project_folder(answers, destination)
    while site_path.exists():
        console.print(
            f"The folder {str(site_path)!r} already exists. Please choose a different name.", style="red", markup=False
        )
        answers["project_slug"], site_path = ask_project_folder(answers, destination)
    answers["app_filename"] = ask(answers, "app_filename", "App file name")
    answers["site_variable"] = ask(answers, "site_variable", "Name of the Site variable in the app file")
    answers["output_path"] = ask(answers, "output_path", "Folder for the built site")
    answers["include_collection"] = ask(answers, "include_collection", "Include an example collection?")
    answers["include_blog"] = ask(answers, "include_blog", "Include an example blog?")
    answers["include_cli"] = ask(answers, "include_cli", "Use the Render Engine CLI?")
    return InitOptions(**answers)


def extra_context(text: str) -> dict[str, Any]:
    """Read the answers given with `--extra-context`, a JSON object like '{"site_title": "My Blog"}'.

    :param text: The text given with `--extra-context`.
    :return: The answers.
    :raises ArgumentTypeError: If the text isn't a JSON object, or has unknown or invalid answers.
    """
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
    """Read `--output-dir`: the folder to create the project in. It's created if it doesn't exist.

    :param text: The text given with `--output-dir`.
    :return: The folder.
    :raises ArgumentTypeError: If the path is a file.
    """
    path = Path(text)
    if path.exists() and not path.is_dir():
        raise ArgumentTypeError(f"{text!r} is a file, not a folder")
    return path


def main(argv: list[str] | None = None, prog: str = "render-engine-init") -> None:
    """Create a new Render Engine site from the command line.

    Asks the questions for the new site, or uses the default answers with `--no-input`,
    and creates the project folder inside the destination folder. Errors are shown
    without a traceback, and exit with code 1 (or 130 when cancelled with Ctrl+C).

    :param argv: The command-line arguments. Defaults to `sys.argv[1:]`.
    :param prog: The program name shown in the help, e.g. `render-engine init` when
        called from render-engine-cli.
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
