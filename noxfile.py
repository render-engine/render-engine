import nox

PYTHON_VERSIONS = ["3.15", "3.14", "3.13", "3.12", "3.11"]


@nox.session(python=PYTHON_VERSIONS, venv_backend="uv", reuse_venv=True)
def test(session: nox.Session) -> None:
    """Run the test suite"""
    session.run_install(
        "uv",
        "sync",
        "--dev",
        "--quiet",
        external=True,
    )
    session.run("pytest", "tests")
