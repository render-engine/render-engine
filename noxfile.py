import nox

PYTHON_VERSIONS = ["3.14", "3.13", "3.12", "3.11", "3.10"]


@nox.session(python=PYTHON_VERSIONS, venv_backend="uv")
def test(session: nox.Session) -> None:
    """Run the test suite"""
    session.run_install(
        "uv",
        "sync",
        "--extra",
        "dev",
        "--quiet",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
        external=True,
    )
    session.run("pytest", "tests")
