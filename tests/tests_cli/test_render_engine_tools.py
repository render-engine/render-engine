import pathlib

from render_engine.cli.cli import remove_output_folder
from render_engine.site import Site


def test_clean_folder(tmp_path):
    site = Site()
    site.output_path = tmp_path
    dirty_output_path = tmp_path / "test"  # Tests that nested folders are also removed
    dirty_output_path.mkdir()
    dirty_output_path.joinpath("test.txt").touch()
    assert dirty_output_path.exists()

    remove_output_folder(pathlib.Path(dirty_output_path))
    assert not dirty_output_path.exists()
    assert not list(tmp_path.iterdir())
