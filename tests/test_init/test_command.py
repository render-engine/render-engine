"""Tests for `render-engine init` on the command line (`main` in `__main__.py`).

These tests run the command with flags and typed answers (`sys.argv` and `sys.stdin` are
replaced for each test) and check what the user sees: the questions, asking again after
an invalid answer, `--no-input`, `--extra-context`, error messages without
tracebacks, exit codes and cancelling.

Which answers are valid is tested in `test_options.py`; these tests only check that the
command handles valid and invalid answers correctly.
"""

import io
import subprocess
import sys

import pytest
from rich.prompt import Prompt

from render_engine.init.__main__ import main


def run_init(monkeypatch, *args, answers=""):
    """Run `render-engine init` with the given flags, typing `answers` into the questions."""
    monkeypatch.setattr(sys, "argv", ["render-engine-init", *args])
    monkeypatch.setattr(sys, "stdin", io.StringIO(answers))
    main()


# Without questions


def test_no_input_uses_the_defaults(monkeypatch, tmp_path, capsys):
    run_init(monkeypatch, "--no-input", "-o", str(tmp_path))

    assert (tmp_path / "untitled-site" / "app.py").is_file()
    assert f"Created your new site in {tmp_path / 'untitled-site'}" in capsys.readouterr().out


def test_extra_context_is_used_with_no_input(monkeypatch, tmp_path):
    run_init(monkeypatch, "--no-input", "-o", str(tmp_path), "-e", '{"site_title": "My Blog", "include_blog": false}')

    assert (tmp_path / "my-blog" / "content" / "pages").is_dir()
    assert not (tmp_path / "my-blog" / "content" / "blog").exists()


# With questions


def test_answers_are_used(monkeypatch, tmp_path):
    # title, URL, folder name, app file, output folder, collection, blog, CLI
    answers = "My Blog\n\n\nmain.py\n\nn\n\n\n"

    run_init(monkeypatch, "-o", str(tmp_path), answers=answers)

    site_path = tmp_path / "my-blog"
    assert (site_path / "main.py").is_file()
    assert not (site_path / "content" / "pages").exists()
    assert (site_path / "content" / "blog").is_dir()


def test_extra_context_sets_the_defaults(monkeypatch, tmp_path):
    run_init(monkeypatch, "-o", str(tmp_path), "-e", '{"site_title": "From Extra"}', answers="\n" * 8)

    assert (tmp_path / "from-extra").is_dir()


def test_invalid_answer_is_asked_again(monkeypatch, tmp_path, capsys):
    # the first URL is invalid, the second one is fine
    answers = "My Blog\nexample.com\nhttps://my-blog.dev\n" + "\n" * 6

    run_init(monkeypatch, "-o", str(tmp_path), answers=answers)

    assert "must start with http" in capsys.readouterr().out
    assert "https://my-blog.dev" in (tmp_path / "my-blog" / "app.py").read_text()


def test_existing_folder_is_asked_again(monkeypatch, tmp_path, capsys):
    (tmp_path / "untitled-site").mkdir()
    # keep the title and URL, then the default folder exists, so pick another one
    answers = "\n\n\nsecond-try\n" + "\n" * 5

    run_init(monkeypatch, "-o", str(tmp_path), answers=answers)

    assert "already exists" in capsys.readouterr().out
    assert (tmp_path / "second-try").is_dir()


# Errors


def test_error_is_shown_as_one_line(monkeypatch, tmp_path, capsys):
    (tmp_path / "untitled-site").mkdir()

    with pytest.raises(SystemExit) as exit_info:
        run_init(monkeypatch, "--no-input", "-o", str(tmp_path))

    assert exit_info.value.code == 1
    output = capsys.readouterr().err
    assert output.startswith("Couldn't create the site: The folder")
    assert output.count("\n") == 1


@pytest.mark.parametrize(
    "args, message",
    [(["-o", "notes.txt"], "'notes.txt' is a file")],
)
def test_invalid_folder_is_rejected_before_the_questions(monkeypatch, tmp_path, capsys, args, message):
    (tmp_path / "notes.txt").write_text("not a folder")
    monkeypatch.chdir(tmp_path)

    with pytest.raises(SystemExit) as exit_info:
        run_init(monkeypatch, *args)

    assert exit_info.value.code == 2
    output = capsys.readouterr()
    assert message in output.err
    assert "Site title" not in output.out


def test_invalid_extra_context_is_rejected(monkeypatch, tmp_path, capsys):
    with pytest.raises(SystemExit) as exit_info:
        run_init(monkeypatch, "--no-input", "-o", str(tmp_path), "-e", '{"title": "My Blog"}')

    assert exit_info.value.code == 2
    assert "unknown answers title" in capsys.readouterr().err


def test_input_ending_early_creates_nothing(monkeypatch, tmp_path, capsys):
    # the input ends after the title, like a script that gives too few answers, or pressing Ctrl-D
    with pytest.raises(SystemExit) as exit_info:
        run_init(monkeypatch, "-o", str(tmp_path), answers="My Blog\n")

    assert exit_info.value.code == 1
    assert "The input ended before all questions were answered" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


def test_ctrl_c_during_the_questions_creates_nothing(monkeypatch, tmp_path, capsys):
    def interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(Prompt, "ask", interrupt)

    with pytest.raises(SystemExit) as exit_info:
        run_init(monkeypatch, "-o", str(tmp_path))

    assert exit_info.value.code == 130
    assert "Cancelled" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


# Running it as a command
def test_usage_shows_the_command_name(monkeypatch, capsys):
    # on Python 3.11-3.13, `python -m render_engine.init` passes the path of `__main__.py` as the program name
    monkeypatch.setattr(sys, "argv", ["/path/to/render_engine/init/__main__.py", "--help"])

    with pytest.raises(SystemExit):
        main()

    assert capsys.readouterr().out.startswith("usage: render-engine-init ")


def test_module_can_be_run(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "render_engine.init", "--no-input", "-o", str(tmp_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "untitled-site").is_dir()


def test_long_error_message_is_not_broken_into_lines(monkeypatch, tmp_path, capsys):
    destination = tmp_path / ("very-long-folder-name-" * 5)
    (destination / "untitled-site").mkdir(parents=True)

    with pytest.raises(SystemExit):
        run_init(monkeypatch, "--no-input", "-o", str(destination))

    assert str(destination / "untitled-site") in capsys.readouterr().err


def test_arguments_can_be_passed_directly(tmp_path):
    main(["--no-input", "-o", str(tmp_path)])

    assert (tmp_path / "untitled-site").is_dir()


def test_program_name_can_be_changed(capsys):
    with pytest.raises(SystemExit):
        main(["--help"], prog="render-engine init")

    assert capsys.readouterr().out.startswith("usage: render-engine init ")


def test_template_option_is_rejected(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["-t", "my-template"])

    assert exit_info.value.code == 2
    assert "unrecognized arguments: -t" in capsys.readouterr().err


def test_help_says_custom_templates_are_not_supported(capsys):
    with pytest.raises(SystemExit):
        main(["--help"])

    assert "Custom templates (--template) are no longer supported." in capsys.readouterr().out
