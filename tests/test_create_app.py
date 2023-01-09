import pathlib

import pytest

import render_engine.cli as cli
from render_engine.site import Site


def test_create_site_with_vars():
    """Tests the site can be built with optional attributes""" ""
    site = cli._create_site_with_vars(
        site_title="title",
        site_url="url",
        site_description="description",
        site_author="author",
        collection_path="collections_path",
    )

    assert site.site_vars["site_title"] == "title"
    assert site.site_vars["site_url"] == "url"
    assert site.site_vars["site_description"] == "description"
    assert site.site_vars["site_author"] == "author"
    assert site.site_vars["collections_path"] == "collections_path"


def test_create_folder(mocker):
    """Tests folder can be created"""
    mocker.patch("render_engine.cli.pathlib.Path.mkdir")
    app_folder = cli._create_folder(
        folder=pathlib.Path("mytest_folder"),
        overwrite=True,
    )

    cli.pathlib.Path.mkdir.called_once_with(
        parents=True,
        exist_ok=True,
    )

    assert app_folder == cli.pathlib.Path("mytest_folder")


def test_create_app(tmp_path):
    """Tests that the app.py is created"""
    d = tmp_path

    cli.init(
        site_title="title",
        site_url="url",
        site_description="description",
        site_author="author",
        project_folder=d,
    )

    assert (
        d.joinpath("app.py").read_text().strip()
        == pathlib.Path("tests/create_app_check_file.txt").read_text().strip()
    )
