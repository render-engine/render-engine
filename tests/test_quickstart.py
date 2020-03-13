from render_engine import quickstart

import shutil
from pathlib import Path

def test_create_templates_directory_does_not_exist():
    # setup
    path = Path("./tests/quickstart/templates/")

    if path.is_dir():
        shutil.rmtree(path)

    # test
    quickstart.create_templates_directory("./tests/quickstart", "templates")
    assert path.is_dir()

    # cleanup
    shutil.rmtree(path)

