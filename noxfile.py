import nox

PYTHON_VERSIONS = ["3.13", "3.12", "3.11", "3.10"]


@nox.session
def lint(session, python="3.12"):
    """Lint using ruff"""

    session.install("ruff")
    session.run("ruff", "check", "--fix", "src")
    session.run("ruff", "format", "src")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run the test suite"""
    session.install("pytest")
    session.install("-r", "requirements.txt")
    session.run("pytest", "tests")
