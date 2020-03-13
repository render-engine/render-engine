from render_engine import quickstart

import shutil
import pytest
from pathlib import Path


def test_create_content_path_does_not_exist():
    # setup
    path = Path('./tests/content')

    if path.is_dir():
        shutil.rmtree(path)

    #test
    quickstart.create_output_path('./tests', 'content')
    assert path.is_dir()

    # cleanup
    shutil.rmtree(path)


def test_create_content_path_does_exists():
    # setup
    path = Path('./tests/content')
    path.mkdir()

    #test
    quickstart.create_output_path('./tests', 'content')
    assert path.is_dir()

    # cleanup
    shutil.rmtree(path)


def test_create_templates_path_does_not_exist():
    # setup
    path = Path('./tests/templates')

    if path.is_dir():
        shutil.rmtree(path)

    #test
    quickstart.create_output_path('./tests', 'templates')
    assert path.is_dir()

    # cleanup
    shutil.rmtree(path)




def test_create_templates_path_does_exists():
    # setup
    path = Path('./tests/templates')
    path.mkdir()

    #test
    quickstart.create_output_path('./tests', 'templates')
    assert path.is_dir()

    # cleanup
    shutil.rmtree(path)
