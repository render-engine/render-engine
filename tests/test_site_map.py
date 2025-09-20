from collections import defaultdict

import pytest

from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.site import Site
from render_engine.site_map import SiteMap

PAGE_TEMPLATE = """
---
title: {title}
slug: {slug}
---
{title}
"""


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    tmp_output_path = tmp_path_factory.getbasetemp() / "test_output"
    tmp_input_path = tmp_path_factory.getbasetemp() / "content"
    tmp_input_path.mkdir(parents=True)

    coll_pages = defaultdict(list)
    for collection in ["coll1", "coll2"]:
        for n in range(4):
            coll_pages[collection].append(
                Page(content=PAGE_TEMPLATE.format(title=f"{collection} -- Page {n}", slug=f"page{n}"))
            )
    for n in range(3):
        content_file = tmp_input_path / f"page{n}.md"
        content_file.write_text(PAGE_TEMPLATE.format(title=f"Page {n}", slug=f"page{n}"))

    class testSite(Site):
        output_path = tmp_output_path

    site = testSite()

    for collection in ["coll1", "coll2"]:

        class MyColl(Collection):
            routes = [collection]
            pages = coll_pages[collection]

        collection_class = MyColl
        collection_class.__name__ = collection
        site.collection(collection_class)

    for n in range(3):

        @site.page
        class MyPage(Page):
            content_path = tmp_input_path / f"page{n}.md"

    yield site


def test_site_map_to_html(site):
    sm = SiteMap(site.route_list, "")
    assert sm.html == (
        "<ul>\n"
        '\t<li><a href="/coll1">coll1</a></li>\n'
        "\t<ul>\n"
        '\t\t<li><a href="/coll1/page0.html">coll1 -- Page 0</a></li>\n'
        '\t\t<li><a href="/coll1/page1.html">coll1 -- Page 1</a></li>\n'
        '\t\t<li><a href="/coll1/page2.html">coll1 -- Page 2</a></li>\n'
        '\t\t<li><a href="/coll1/page3.html">coll1 -- Page 3</a></li>\n'
        "\t</ul>\n"
        '\t<li><a href="/coll2">coll2</a></li>\n'
        "\t<ul>\n"
        '\t\t<li><a href="/coll2/page0.html">coll2 -- Page 0</a></li>\n'
        '\t\t<li><a href="/coll2/page1.html">coll2 -- Page 1</a></li>\n'
        '\t\t<li><a href="/coll2/page2.html">coll2 -- Page 2</a></li>\n'
        '\t\t<li><a href="/coll2/page3.html">coll2 -- Page 3</a></li>\n'
        "\t</ul>\n"
        '\t<li><a href="/page0.html">Page 0</a></li>\n'
        '\t<li><a href="/page1.html">Page 1</a></li>\n'
        '\t<li><a href="/page2.html">Page 2</a></li>\n'
        "</ul>\n"
    )


@pytest.mark.parametrize(
    "attr, value, params, expected",
    [
        ("slug", "page1", {}, "/page1.html"),
        ("slug", "page3", {}, None),
        ("slug", "page3", {"full_search": True}, "/coll1/page3.html"),
        ("slug", "page3", {"collection": "coll2"}, "/coll2/page3.html"),
        ("path_name", "page1.html", {}, "/page1.html"),
        ("path_name", "page3.html", {}, None),
        ("path_name", "page3.html", {"full_search": True}, "/coll1/page3.html"),
        ("path_name", "page3.html", {"collection": "coll2"}, "/coll2/page3.html"),
        ("slug", "page1", {}, "/page1.html"),
        ("slug", "page3", {}, None),
        ("slug", "page3", {"full_search": True}, "/coll1/page3.html"),
        ("slug", "page3", {"collection": "coll2"}, "/coll2/page3.html"),
        ("title", "Page 1", {}, "/page1.html"),
        ("title", "coll1 -- Page 3", {}, None),
        ("title", "coll1 -- Page 3", {"full_search": True}, "/coll1/page3.html"),
        ("title", "coll1 -- Page 3", {"collection": "coll2"}, None),
        ("title", "coll2 -- Page 3", {"collection": "coll2"}, "/coll2/page3.html"),
    ],
)
def test_site_map_search(site, attr, value, params, expected):
    sm = SiteMap(site.route_list, "")
    if expected is not None:
        found = sm.find(attr, value, **params)
        assert found.url_for == expected
    else:
        assert sm.find(attr, value, **params) is None
