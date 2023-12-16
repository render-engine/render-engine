import pytest
from render_engine.cli import cli

@pytest.fixture(scope="module")
def test_template(tmp_path_factory):
    test_template = tmp_path_factory.getbasetemp().joinpath("test_template")
    test_template.mkdir()
    test_template.joinpath("cookiecutter.json").write_bytes(
        b'{"project_slug": "test_template"}'
    )
    cc_path = test_template.joinpath("{{cookiecutter.project_slug}}")
    cc_path.mkdir()
    cc_path.joinpath("app.py").write_bytes(
        b"""print("hello world")""",
    )
    return test_template.resolve()


def test_init_local_path(test_template, tmp_path):
    """Tests that you can call init using a local path"""
    cli.init(
        template=str(test_template),
        no_input=True,
        output_dir=tmp_path,
    )
    template_path = tmp_path.joinpath("test_template")
    app_py = template_path.joinpath("app.py")
    assert app_py.exists()
    assert app_py.read_bytes() == b'print("hello world")'
