---
title: "Contributing to Render Engine"
description: "This document will help you get started in contributing to the Render Engine codebase is open source and contributions are welcome."
date: August 22, 2024
tags: ["contribution", "guide", "open-source", "render-engine"]
---

This document will help you get started in contributing to the Render Engine codebase is open source and contributions are welcome.

> **NOTE**
> This Document is specifically for contributing to the Render-Engine package. For help with creating a plugin, custom parser or Theme. Please check the [Render Engine Wiki](https://github.com/render-engine/.github/wiki) or the [Render Engine Docs](https://render-engine.readthedocs.org).

## The Docs

This document is meant to help users get started in contributing to Render-Engine and isn't a replacement for the more in-depth knowledge in the docs. You can find the docs at <https://render-engine.readthedocs.org>

## Code of Conduct

Render Engine and all of the packages created under the Render Engine Org follow the same [Code of Conduct](https://github.com/render-engine/render-engine/blob/main/.github/CODE_OF_CONDUCT.md). Contributors to this project are expected to adhere to this code of conduct when working with this project.

## Instead of Making a Change in Render Engine's Code Consider

Render Engine is working to build a rich ecosystem of products that allow for more customizability within the platform. When suggesting a feature, consider the following:

### Is this better as a Plugin?

Plugins allow you to add features to render engine that allow for custom functionality in in a site.

You can learn more about Plugins and see examples in the [wiki](https://github.com/render-engine/.github/wiki/plugins)

### Would your feature be a good theme?

Themes allow you to create a foundation for the design of the website.

You can learn more about Themes and see examples in the [wiki](https://github.com/render-engine/.github/wiki/themes)

### Are you trying to create support for a new data type?

Custom Parsers & Collections allow you to take all kinds of data types and convert them into one or more HTML pages.

You can learn more about Custom Parsers and Collections and see examples in the [wiki](https://github.com/render-engine/.github/wiki/Custom-Collections-and-Parsers)

### Sometimes the lines blur

Often themes can require plugins and some plugins will work best with custom parsers and collections. There is nothing wrong with making a package that contains more than one of these features.

There is one advantage to a singular package and that is reusability.

For instance instead of including tailwindcss into your project and all the code required to support it. You can just require the [tailwindcss plugin](https://github.com/kjaymiller/render-engine-tailwindcss) in your theme.

---

If you submit an issue that could be solved as a plugin, theme, or custom parser or collection, your issue will be closed with a friendly explanation as to why.

## Filing an Issue

> **There is no issue too small to be an issue**

If you see or experience a problem, please file an issue. Include any important information as it is relevant such as:

- Operating System - *System and Version (e.g. MacOS Sonoma)*
- Python Version - *ex. Python 3.12.0*
- Plugins/Themes/Custom Parsers & Collections Installed - *You can add them as a list*
- Commands/Code Used - *What did you enter to get the output that you received*
- Output - *Copy the Error or output that you receive. This can be a screenshot but is more helpful as text*

## Working on an Issue

> **EVERY BUG/APPLICABLE FEATURE SHOULD BE FILED AS AN ISSUE**

### Issue vs Discussion

If you don't know what the **solution** is, that's okay, we can work on getting a solution.

If you aren't sure what the **problem** is, create a [discussion](https://github.com/render-engine/render-engine/discussion) post and we can talk about it.

If you aren't sure if it should be a discussion or an issue... That's okay, GitHub allows us to transfer issues into discussions or vice-versa.

The general rule of thumb is don't let, not knowing where it goes, be the thing that prevents you from reporting that something happened. If you create an issue or a discussion, we'll address it/move it to the necessary place!

### Being assigned an issue

It's important to wait to be assigned an issue before starting to work on it. This prevents the following scenarios:

> Two individuals contribute solutions to the same issue and someone is left with their code not being accepted.
> A contributor does the work to resolve an issue  that is ultimately marked as *closed-Not Planned*. will not be added to the code base.
> A contributor does work when a different solution is considered, resulting in wasting the contributor's time.

If you want to work on a project simply say "I can work on this" or something to that effect, and wait for one of the maintainers to assign the issue to you.

Once you've been [assigned an issue](./CONTRIBUTING.md/#being-assigned-an-issue), you can begin working on an issue either locally with a [manual setup](./environment_setup.md#developing-locally) or [dev container](./environment_setup.md#using-dev-containers) or using [GitHub Codespaces](./environment_setup.md#using-codespaces).

## What Should your contribution have

### Your changes linted and formatted using ruff and markdownlint

Render engine's style is defined in the projects `pyproject.toml`. Before submitting your pull request. You should run the following commands. (If you don't a commit will be added to your PR doing so or you will be asked to before committing.)

```sh
python -m ruff check src --fix
python -m ruff format src
```

Markdown changes will also be linted using the markdownlint2 github action. If you are using our dev container or code space, the markdownlint extension will update changes on save.

### Tests for your code additions and removals

- Include at least one test case using [pytest](https://docs.pytest.org/en/7.1.x/getting-started.html) showing that your code works as intended. More tests should be added as needed.

Additions should have new tests in the appropriate file based on where the change was made.

Removal of code should likely have a regression test (that is a test that ensures the behavior that you're trying to fix does not show back up).

### Make sure your changes aren't breaking existing code

Ensure that all existing tests pass and no new tests are skipped unless expressly told to skip them.

Ensure that new dependencies are listed, justified, and approved to be added.

### Document as much as possible

New Attributes or features should be properly documented using the [Documentation Guidelines](#contributing-to-documentation).

## Contributing to Documentation

Render Engine uses [readthedocs](https://readthedocs.org) in combination with
[MkDocs](https://www.mkdocs.org),[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), and [mkdocsstrings](https://mkdocsstrings.readthedocs.io/en/latest/) to generate documentation.

When you are updating a function, method, or class be sure to update the docstring with any necessary changes.

If you're documenting a process be sure to include images and gifs where necessary. Assets should be stored in the `docs/docs/assets` folder.

## Formatting your PR

Render Engine uses a Pull Request Template that will help you include all the information needed to submit your PR.

If you're starting from a blank PR be sure to include the following:

### A descriptive name of the changes

### outline which issue(s) and discussions are being addressed

In most cases, each PR should address one issue unless previously discussed with one of the maintainers.

### Mention documentation and tests that were added or updated

Also mention if there are any follow up tasks that still need to happen.
