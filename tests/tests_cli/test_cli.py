import pytest

from render_engine import Page, Site
from render_engine.cli.cli import get_site_content_paths


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    class FakeSite(Site):
        output_path = tmp_path_factory.getbasetemp() / "output_path"

    site = FakeSite()

    content_path1 = tmp_path_factory.getbasetemp() / "test_content_path1.txt"
    content_path1.write_text("Hello Wold")

    content_path2 = tmp_path_factory.getbasetemp() / "test_content_path2.txt"
    content_path2.write_text("Hello Space")

    @site.page
    class FakePage1(Page):
        content_path = content_path1

    @site.page
    class FakePage2(Page):
        content_path = content_path2

    return site


def test_get_site_content_path(site, tmp_path_factory):
    """Tests that the paths returned from the pages"""

    content_path1 = tmp_path_factory.getbasetemp() / "test_content_path1.txt"
    content_path2 = tmp_path_factory.getbasetemp() / "test_content_path2.txt"

    assert get_site_content_paths(site) == [content_path1, content_path2]


@pytest.mark.skip("Not sure how to test importlib")
def test_import_lib_gets_site():
    pass
