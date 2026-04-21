# Contributing to Render Engine

This document will help you get started in contributing to the Render Engine codebase is open source and
contributions are welcome.

> **NOTE**
> This is specifically for contributing to the Render-Engine package. For help with creating a plugin, custom
> parser or Theme. Please check the [Render Engine Wiki][wiki] or the [Render Engine Docs][docs].

## Docs

Docs can be found at <https://render-engine.readthedocs.org>

## Code of Conduct

Render Engine and all of the packages in this org follow the same [Code of Conduct].

## Before you Contribute

When suggesting a feature, consider the following:

- Is this better as a Plugin?
- Would your feature be a good theme?
- Could this be implemented as a Custom Parsers or Collections

More on when to choose these solutions in our [docs][docs-contributing].

## Filing an Issue

> **There is no issue too small to be an issue**

If you see or experience a problem, please file an issue. Include any important information as it is relevant such as:

- Summary of Actions
- Operating System
- Python Version
- Plugins/Themes/Custom Parsers & Collections Installed
- Commands/Code Used
- Output
- [AI Attestation][ai-attestation]

## Wait to be Assigned Issues

It's important to wait to be assigned an issue before starting to work on it. This prevents
[working on code that won't be merged][being-assigned].

Comment _I can work on this_ or something to that effect, and wait for one of the maintainers to assign the issue to you.

## Setup your Environment

Once you've been [assigned an issue][being-assigned], you can begin working on an issue either locally with:

- [manual setup][manual-setup]
- [dev container][dev-container]/[GitHub Codespaces][codespaces].
- from dockerfile

### Manual Configuration

- fork and clone
- create virtual environment and connect to virtual environment
- create local installation with dev tooling
  `python -m pip install -e .[dev]`
- run pre-commit (it will install all of its needed deps)

### Dockerfile

Our DevContainer is built primarily from a dockerfile. You can build from our Dockerfile directly which would
ensure the manual configuration is ran (You will still need to fork and clone).

## Verify Before Submitting

Render Engine uses nox to text against all supported versions. PRs will not be approved without tests passing on
all supported versions.

- 🚫 changes aren't breaking existing code (failing tests)
- 🚫 Ensure new dependencies are listed, justified, and approved to be added.

## TODOs

Todos are not encouraged all the time but if necessary please indicate any todos with the `# TODO` prefix.
We use [todo-to-issue] as a GitHub Action to create issues from TODOs.

When a PR containing `# TODO` comments is opened, a bot will comment suggesting a maintainer
add the **todo-to-issue** label. Once a maintainer adds the label, the action will:

1. Create GitHub issues for each TODO
2. Update the TODO comments in your code with the issue number and link
3. Commit the changes back to your PR branch

The label is removed automatically afterward and can be re-applied if new TODOs are added.

## Contributing to Documentation

Render Engine uses [readthedocs][readthedocs] in combination with [MkDocs][mkdocs],
[Material for MkDocs][material], and [mkdocsstrings][mkdocsstrings] to generate documentation.

- 📝 update docstrings for functions, methods, and classes.
- 📷 add images and gifs where necessary. Assets should be stored in the `docs/docs/assets` folder.

Test your docs changes by running the command **FROM THE PROJECT ROOT**.

### Using Just (recommended)

You can start the documentation server on the default port (8000):
```sh
just docs 
```
Or, you can specify a custom port:
```sh
just docs 8080
```
> **NOTE** Please make sure you have installed the `docs` dependency group before running this command.

```
uv sync --group docs
```

## Formatting your PR

Render Engine uses a Pull Request Template that will help you include all the information needed to submit your PR.

If you're starting from a blank PR be sure to include the following:

- Summary
- issue(s)/discussions being addressed
- Documentation or tests added/updated
- Any follow up tasks pending
- [AI Attestation][ai-attestation]

When submitting your PR, please be sure to use the template provided.
**Not following this guideline will result in the immediate rejection of your PR.**

## AI Attestation

Projects in the [Render Engine organization][gh-render-engine] will accept code contributions created with the
assistance of AI Coding software. We ask that that you include an AI Attestation to your issue, comment, or PR.

This attestation should mean that the AI model is included as a co-Author of the changes.

The AI assistant is your copilot. You are still responsible for code changes submitted.
Low quality contributions or code that cannot be defended by the USER (not their AI model)
will result in issues/prs being immediately closed.
Multiple low quality contributions will result in your user account being banned from contribution.

[ai-attestation]: #ai-attestation
[gh-render-engine]: https://github.com/render-engine
[wiki]: https://github.com/render-engine/.github/wiki
[docs]: https://render-engine.readthedocs.org
[being-assigned]: https://render-engine.readthedocs.io/en/latest/contributing/CONTRIBUTING/#being-assigned-an-issue
[manual-setup]: https://render-engine.readthedocs.io/en/latest/contributing/environment_setup#developing-locally
[dev-container]: https://render-engine.readthedocs.io/en/latest/contributing/environment_setup#developing-locally
[codespaces]: https://render-engine.readthedocs.io/en/latest/contributing/environment_setup#using-codespaces
[readthedocs]: https://readthedocs.org
[mkdocs]: https://www.mkdocs.org
[material]: https://squidfunk.github.io/mkdocs-material/
[mkdocsstrings]: https://mkdocsstrings.readthedocs.io/en/latest/
[code of conduct]: https://github.com/render-engine/render-engine/blob/main/.github/CODE_OF_CONDUCT.md
[docs-contributing]: https://render-engine.readthedocs.io/en/latest/contributing/CONTRIBUTING/#instead-of-making-a-change-in-render-engines-code-consider
[todo-to-issue]: https://github.com/marketplace/actions/todo-to-issue
