import pytest
import render_engine.cli as _cli

pytest.fixture()
def get_tmp_path(tmp_path_facorty, folder):
    return tmp_path_factory.getbasetemp() / folder

@pytest.fixture(scope="session")
def default_cli(tmp_path_factory):
    project_folder = tmp_path_factory.getbasetemp() / "test_default_cli_app"
    project_folder.mkdir()
    output_path = tmp_path_factory.getbasetemp() / "default_cli_output"

    _cli.init(
        collection_path="pages",
        project_folder=project_folder,
        site_title="Test Site",
        site_url="http://localhost:8000",
        site_description="Test Site Description",
        author_name="Test Site Author",
        author_email="hello@example.com",
        output_path=output_path
    )

@pytest.fixture(scope="session")
def skip_collection_cli(tmp_path_factory):
    project_folder = tmp_path_factory.getbasetemp() / "test_skip_collection_cli_app"
    project_folder.mkdir()
    output_path = tmp_path_factory.getbasetemp() / "default_skip_collection_cli_output"

    _cli.init(
        skip_collection=True,
        project_folder=project_folder,
        site_title="Test Site",
        site_url="http://localhost:8000",
        site_description="Test Site Description",
        author_name="Test Site Author",
        author_email="hello@example.com",
        output_path=output_path
    )
