from argparse import ArgumentParser
from pathlib import Path


def main():
    parser = ArgumentParser(description="Create a new site configuration.")
    # parser.add_argument(
    #     "-e",
    #     "--extra-context",
    #     default=None,
    #     help="Extra context to pass to the cookiecutter template. This must be a JSON string.",
    # )
    # parser.add_argument(
    #     "-t",
    #     "--template",
    #     default="https://github.com/render-engine/cookiecutter-render-engine-site",
    #     help="Template to use for creating a new site.",
    # )
    parser.add_argument(
        "--no-input",
        action="store_true",
        help="Do not prompt for parameters.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("./"),
        help="Directory to create the new site configuration in.",
    )
    # parser.add_argument(
    #     "-c",
    #     "--config-file",
    #     type=Path,
    #     default=None,
    #     help="Path to the cookiecutter config file to use.",
    # )
    args = parser.parse_args()
    init(
        template=args.template,
        extra_context=args.extra_context,
        no_input=args.no_input,
        output_dir=args.output_dir,
        config_file=args.config_file,
    )


def init(template: str, extra_context: str | None, no_input: bool, output_dir: Path, config_file: Path | None):
    """
    Create a new site configuration. You can provide extra_context to the template.

    The template can be a local path or a git repository.
    """

    raise NotImplementedError("Site generation is not implemented yet.")


if __name__ == "__main__":
    main()
