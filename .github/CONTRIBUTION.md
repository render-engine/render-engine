# Contribution

Render Engine is open source and contributions are welcome.

Below are the steps for contributing to the project.

For code contributions. Please complete the following steps.

## Submit Issue with **feature** or **bugfix** label. Issue should use story

like verbage. Ex:

### Features
>
> When I do/call <CODE FOR FEATURE>, I would like <OUTCOME FOR FEATURE>. This
> would <EXPLANATION OF WHY YOU THINK FEATURE WOULD BE GREAT>.

### Bugs
>
> When I do/call <CODE causing Bug>, <THE BUG HAPPENING> when I would expect
> <EXPECTED OUTCOME>.

## Providing Code for your Contribution

- Include a test case using pytest showing that your code works as intended.
- Ensure that all existing tests pass unless you are correcting the behavior of
  a feature previously tested.
- Ensure that new dependencies are listed and justified.
- Your PR should outline which issue is being addressed and one issue per PR
  should be submitted.
- New Attributes or features should be properly documented using the
  Documentation guidelines.

## Style Guidelines

Render Engine uses two modules to style code.

- [isort](https://github.com/timothycrosley/isort)
- [black](https://github.com/psf/black)

Code should follow the stylings from isort and black before merged. This can be
done by executing the following command (with both modules installed).

`$render_engine> noisort render_engine --profile=black && black render_engine`

## Contributing to Documentation

Render Engine uses [readthedocs](https://readthedocs.org) in combination with
[MkDocs](https://www.mkdocs.org),[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), and [mkdocsstrings](https://mkdocsstrings.readthedocs.io/en/latest/) to generate documentation.