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


If you submit an issue that could be solved as a plugin, theme, or custom parser or collection, your issue will be closed with a friendly explanation as to why.

## Filing an Issue

**There is no issue too small to be an issue**

If you see or experience a problem, please file an issue. Include any important information as it is relevant such as:

```md
## Summary of Actions
## Operating System 
System and Version (e.g. MacOS Sonoma)

## Python Version
Python 3.12.0

## Plugins/Themes/Custom Parsers & Collections Installed

- Plugin1
- Theme2

## Commands/Code Used 

What did you enter to get the output that you recieved

## Output

Copy the Error or output that you recieve.

This can be a screenshot but is more helpful as text*
```

## Working on an Issue

**Every bug/applicable feature should be filed as an Issue. _When in doubt, file an issue_"

It's important to wait to be assigned an issue before starting to work on it. This prevents the following scenarios:

> Two individuals contribute solutions to the same issue and someone is left with their code not being accepted.

> A contributor does the work to resolve an issue  that is ultimately marked as _closed-Not Planned_. will not be added to the code-base.

> A contributor does work when a different solution is considered, resulting in wasting the contributor's time.

If you want to work on a project simply say "I can work on this" or something to that effect, and wait for one of the maintainers to assign the issue to you.

Once you've been [assigned an issue](https://render-engine.readthedocs.io/en/latest/contributing/contributing#being-assigned-an-issue), you can begin working on an issue either locally with a [manual setup](https://render-engine.readthedocs.io/en/latest/contributing/environment_setup/#developing-locally) or [dev container](https://render-engine.readthedocs.io/en/latest/contributing/environment_setup/#developing-locally) or using [GitHub Codespaces](https://render-engine.readthedocs.io/en/latest/contributing/environment_setup/#using-codespaces).

## Include in Your Contribution

- Your changes linted and formatted using ruff and markdownlint

  ```sh
  python -m ruff lint src --fix
  python -m ruff format src
  ```

  Markdown changes will also be linted using the markdownlint2 github action. If you are using our dev container or code space, the markdownlint extenstion will update changes on save.

- Tests for your code additions and removals
- features and changes are documented

## Verify Before Submitting

- changes aren't breaking existing code (failing tests)
- Ensure that new dependencies are listed, justified, and approved to be added.


## Contributing to Documentation

Render Engine uses [readthedocs](https://readthedocs.org) in combination with
[MkDocs](https://www.mkdocs.org),[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), and [mkdocsstrings](https://mkdocsstrings.readthedocs.io/en/latest/) to generate documentation.

When updating a function, method, or class be sure to update the docstring with any necessary changes.

Include images and gifs where necessary. Assets should be stored in the `docs/docs/assets` folder.

Test your docs changes by running the command **FROM THE PROJECT ROOT**.

```sh
python -m mkdocs serve -f docs/mkdocs.yml
``` 


## Formatting your PR

Render Engine uses a Pull Request Template that will help you include all the information needed to submit your PR. 

If you're starting from a blank PR be sure to include the following:

```md
## Summary

A descriptive name of the changes

## issue(s)/discussions being addressed

In most cases each PR should address one issue unless previously discussed with one of the maintainers.

## Documentation or tests added/updated

You can include the filename and links

## Any follow up tasks pending

So we know not to close any issues that need to be left open
```
