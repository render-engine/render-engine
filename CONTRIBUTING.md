# Contributing to Render Engine

This document will help you get started in contributing to the Render Engine codebase is open source and contributions are welcome.

> **NOTE**
> This is specifically for contributing to the Render-Engine package. For help with creating a plugin, custom parser or Theme. Please check the [Render Engine Wiki](https://github.com/render-engine/.github/wiki) or the [Render Engine Docs](https://render-engine.readthedocs.org).

## Docs

Docs can be found at <https://render-engine.readthedocs.org>

## Code of Conduct

Render Engine and all of the packages in this org follow the same [Code of Conduct](https://github.com/render-engine/render-engine/blob/main/.github/CODE_OF_CONDUCT.md).

## Before you Contribute

When suggesting a feature, consider the following:

- Is this better as a Plugin?
- Would your feature be a good theme?
- Could this be implemented as a Custom Parsers or Collections

More on when to choose these solutions in our [docs](https://render-engine.readthedocs.io/en/latest/contributing/CONTRIBUTING/#instead-of-making-a-change-in-render-engines-code-consider).

## Filing an Issue

> **There is no issue too small to be an issue**

If you see or experience a problem, please file an issue. Include any important information as it is relevant such as:

- Summary of Actions
- Operating System
- Python Version
- Plugins/Themes/Custom Parsers & Collections Installed
- Commands/Code Used
- Output

## Wait to be Assigned Issues

It's important to wait to be assigned an issue before starting to work on it. This prevents [working on code that won't be merged](https://render-engine.readthedocs.io/en/latest/contributing/CONTRIBUTING/#being-assigned-an-issue).

Comment _I can work on this_ or something to that effect, and wait for one of the maintainers to assign the issue to you.

## Setup your Environment

Once you've been [assigned an issue](https://render-engine.readthedocs.io/en/latest/contributing/contributing#being-assigned-an-issue), you can begin working on an issue either locally with:

- [manual setup](https://render-engine.readthedocs.io/en/latest/contributing/environment_setup#developing-locally)
- [dev container](https://render-engine.readthedocs.io/en/latest/contributing/environment_setup#developing-locally)
- [GitHub Codespaces](https://render-engine.readthedocs.io/en/latest/contributing/environment_setup#using-codespaces).

## In Your Contribution

- lint and format code using ruff and markdownlint

  ```sh
  python -m ruff check src --fix
  python -m ruff format src
  ```

- markdownlint extenstion will update changes on save.

- test your code additions and removals
- features and changes are documented

## Verify Before Submitting

- 🚫 changes aren't breaking existing code (failing tests)
- 🚫 Ensure new dependencies are listed, justified, and approved to be added.

## Contributing to Documentation

Render Engine uses [readthedocs](https://readthedocs.org) in combination with
[MkDocs](https://www.mkdocs.org),[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), and [mkdocsstrings](https://mkdocsstrings.readthedocs.io/en/latest/) to generate documentation.

- 📝 update docstrings for functions, methods, and classes.
- 📷 add images and gifs where necessary. Assets should be stored in the `docs/docs/assets` folder.

Test your docs changes by running the command **FROM THE PROJECT ROOT**.

```sh
python -m mkdocs serve -f docs/mkdocs.yml
```

## Formatting your PR

Render Engine uses a Pull Request Template that will help you include all the information needed to submit your PR.

If you're starting from a blank PR be sure to include the following:

- Summary
- issue(s)/discussions being addressed
- Documentation or tests added/updated
- Any follow up tasks pending
