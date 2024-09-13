import pytest

from render_engine.cli import cli


@pytest.fixture(scope="module", autouse=True)
def get_test_template(tmp_path_factory):
    path = tmp_path_factory.getbasetemp()
    project_slug = path.joinpath("{{cookiecutter.project_slug}}")
    project_slug.mkdir()
    project_slug.joinpath("app.py").write_text("hello {{cookiecutter.world}}")
    path.joinpath("cookiecutter.json").write_text('{"world":"world"}')

    return path.resolve()


def tests_error_raised_if_cookiecutter_not_installed(request, mocker):
    """Tests that an error is raised if cookiecutter is not installed"""

    # Mock importing cookiecutter
    mocker.patch("cookiecutter.main.cookiecutter", side_effect=ImportError)

    with pytest.raises(ImportError):
        cli.init(
            extra_context={
                "project_slug": request.node.name,
            },
            template=get_test_template,
            no_input=True,
        )


@pytest.mark.skip("Errors in calling fixture paths")
def test_init_local_path(request, tmp_path):
    """Tests that you can call init using a local path"""

    cli.init(
        extra_context={"project_slug": request.node.originalname},
        template=get_test_template,
        no_input=True,
        output_dir=tmp_path,
    )
    template_path = tmp_path.joinpath(request.node.originalname)
    app_py = template_path.joinpath("app.py")
    assert app_py.exists()
    assert app_py.read_bytes() == b'print("hello world")'


@pytest.mark.skip("Errors in calling fixture paths")
def test_init_called_with_context(request, tmp_path, tmp_path_factory):
    """Tests that you can call init using a local path"""

    temp_file = tmp_path.joinpath("test_cookiecutter_args.json")
    temp_file.write_text(
        f"""
default_context:
    world: "Earth"
    project_slug: {request.node.originalname}
"""
    )

    cli.init(
        template=tmp_path_factory.getbasetemp().resolve(),
        output_dir=tmp_path,
        config_file=temp_file,
        no_input=True,
    )
    template_path = tmp_path.joinpath(request.node.originalname)
    app_py = template_path.joinpath("app.py")
    assert app_py.exists()
    assert app_py.read_bytes() == b'print("hello Earth")'
