from collections import defaultdict

import pytest

from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.site import Site
from render_engine.site_map import SiteMap, SiteMapEntry, StaticSiteMapEntry

PAGE_TEMPLATE = """
---
title: {title}
slug: {slug}
---
{title}
{url}
"""


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    base_temp_path = tmp_path_factory.getbasetemp()
    tmp_output_path = base_temp_path / "test_output"
    tmp_input_path = base_temp_path / "content"
    tmp_input_path.mkdir(parents=True)
    tmp_template_path = base_temp_path / "templates"
    tmp_template_path.mkdir(parents=True)
    template_file_name = "template_file.html"
    template_file = tmp_template_path / template_file_name
    template_file.write_text("{{ content }}\n")

    coll_pages = defaultdict(list)
    for collection in ["coll1", "coll2"]:
        for n in range(4):
            coll_pages[collection].append(
                Page(
                    content=PAGE_TEMPLATE.format(
                        title=f"{collection} -- Page {n}",
                        slug=f"page{n}",
                        url="{{ site_map.find('page0', collection='coll1').url_for }}",
                    )
                )
            )
    for n in range(4):
        content_file = tmp_input_path / f"page{n}.md"
        content_file.write_text(
            PAGE_TEMPLATE.format(
                title=f"Page {n}",
                slug=f"page{n}",
                url="{{ site_map.find('page0', collection='coll1').url_for }}",
            )
        )

    class testSite(Site):
        output_path = tmp_output_path
        _template_path = tmp_template_path

    site = testSite()

    for collection in ["coll1", "coll2"]:

        class MyColl(Collection):
            routes = [f"{collection}-route"]
            pages = coll_pages[collection]

        collection_class = MyColl
        collection_class.__name__ = collection
        site.collection(collection_class)

    for n in range(4):

        @site.page
        class MyPage(Page):
            content_path = tmp_input_path / f"page{n}.md"
            template = template_file_name
            skip_site_map = n == 3
            slug_only_url = n == 2

    yield site


def test_site_map_to_html(site):
    sm = SiteMap("", site.route_list)
    assert sm.html == (
        "<ul>\n"
        '\t<li><a href="/coll1-route">coll1</a></li>\n'
        "\t<ul>\n"
        '\t\t<li><a href="/coll1-route/page0.html">coll1 -- Page 0</a></li>\n'
        '\t\t<li><a href="/coll1-route/page1.html">coll1 -- Page 1</a></li>\n'
        '\t\t<li><a href="/coll1-route/page2.html">coll1 -- Page 2</a></li>\n'
        '\t\t<li><a href="/coll1-route/page3.html">coll1 -- Page 3</a></li>\n'
        "\t</ul>\n"
        '\t<li><a href="/coll2-route">coll2</a></li>\n'
        "\t<ul>\n"
        '\t\t<li><a href="/coll2-route/page0.html">coll2 -- Page 0</a></li>\n'
        '\t\t<li><a href="/coll2-route/page1.html">coll2 -- Page 1</a></li>\n'
        '\t\t<li><a href="/coll2-route/page2.html">coll2 -- Page 2</a></li>\n'
        '\t\t<li><a href="/coll2-route/page3.html">coll2 -- Page 3</a></li>\n'
        "\t</ul>\n"
        '\t<li><a href="/page0.html">Page 0</a></li>\n'
        '\t<li><a href="/page1.html">Page 1</a></li>\n'
        '\t<li><a href="/page2">Page 2</a></li>\n'
        "</ul>\n"
    )


@pytest.mark.parametrize(
    "value, params, expected",
    [
        ("page1", {}, "/page1.html"),
        ("page1", {"attr": "slug"}, "/page1.html"),
        ("page3", {"attr": "slug"}, None),
        ("page3", {"attr": "slug", "full_search": True}, "/coll1-route/page3.html"),
        ("page3", {"attr": "slug", "collection": "coll2"}, "/coll2-route/page3.html"),
        ("page1.html", {"attr": "path_name"}, "/page1.html"),
        ("page3.html", {"attr": "path_name"}, None),
        ("page3.html", {"attr": "path_name", "full_search": True}, "/coll1-route/page3.html"),
        ("page3.html", {"attr": "path_name", "collection": "coll2"}, "/coll2-route/page3.html"),
        ("page1", {"attr": "slug"}, "/page1.html"),
        ("page3", {"attr": "slug"}, None),
        ("page3", {"attr": "slug", "full_search": True}, "/coll1-route/page3.html"),
        ("page3", {"attr": "slug", "collection": "coll2"}, "/coll2-route/page3.html"),
        ("Page 1", {"attr": "title"}, "/page1.html"),
        ("coll1 -- Page 3", {"attr": "title"}, None),
        ("coll1 -- Page 3", {"attr": "title", "full_search": True}, "/coll1-route/page3.html"),
        ("coll1 -- Page 3", {"attr": "title", "collection": "coll2"}, None),
        ("coll2 -- Page 3", {"attr": "title", "collection": "coll2"}, "/coll2-route/page3.html"),
    ],
)
def test_site_map_search(site, value, params, expected):
    sm = SiteMap("", site.route_list)
    if expected is not None:
        found = sm.find(value, **params)
        assert isinstance(found, SiteMapEntry)
        assert found.url_for == expected
    else:
        assert sm.find(value, **params) is None


def test_find_in_template(site):
    site.render()
    assert (site.output_path / "page1.html").read_text() == "Page 1\n/coll1-route/page0.html"


def test_site_map_to_xml(site):
    site.render_xml_site_map = True
    site.render()
    assert (
        (site.output_path / "site_map.xml").read_text()
        == """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url>
	<loc>http://localhost:8000/coll1-route</loc>
</url>
<url>
	<loc>http://localhost:8000/coll1-route/page0.html</loc>
</url>
<url>
	<loc>http://localhost:8000/coll1-route/page1.html</loc>
</url>
<url>
	<loc>http://localhost:8000/coll1-route/page2.html</loc>
</url>
<url>
	<loc>http://localhost:8000/coll1-route/page3.html</loc>
</url>
<url>
	<loc>http://localhost:8000/coll2-route</loc>
</url>
<url>
	<loc>http://localhost:8000/coll2-route/page0.html</loc>
</url>
<url>
	<loc>http://localhost:8000/coll2-route/page1.html</loc>
</url>
<url>
	<loc>http://localhost:8000/coll2-route/page2.html</loc>
</url>
<url>
	<loc>http://localhost:8000/coll2-route/page3.html</loc>
</url>
<url>
	<loc>http://localhost:8000/page0.html</loc>
</url>
<url>
	<loc>http://localhost:8000/page1.html</loc>
</url>
<url>
	<loc>http://localhost:8000/page2</loc>
</url>
</urlset>"""
    )


def test_static_site_map_entry_attributes(tmp_path):
    static_dir = tmp_path / "static"
    (static_dir / "css").mkdir(parents=True)
    file_path = static_dir / "css" / "main.css"
    file_path.write_text("body { color: red; }")

    entry = StaticSiteMapEntry(file_path, static_dir, url_prefix="static")

    assert entry.path_name == "css/main.css"
    assert entry.title == "main.css"
    assert entry.url_for == "/static/css/main.css"
    assert entry.entries == []
    assert str(entry) == entry.url_for


def test_add_static_files_adds_entry_per_file(tmp_path):
    static_dir = tmp_path / "static"
    (static_dir / "images").mkdir(parents=True)
    (static_dir / "style.css").write_text("body{}")
    (static_dir / "images" / "logo.png").write_text("fake-png-bytes")

    sm = SiteMap("http://example.com")
    sm.add_static_files([static_dir])

    urls = sorted(entry.url_for for entry in sm)
    assert urls == ["/static/images/logo.png", "/static/style.css"]


def test_add_static_files_multiple_static_dirs_no_collision(tmp_path):
    static_dir_1 = tmp_path / "static"
    static_dir_2 = tmp_path / "theme_static"
    static_dir_1.mkdir()
    static_dir_2.mkdir()
    (static_dir_1 / "logo.png").write_text("a")
    (static_dir_2 / "logo.png").write_text("b")

    sm = SiteMap("http://example.com")
    sm.add_static_files([static_dir_1, static_dir_2])

    urls = sorted(entry.url_for for entry in sm)
    assert urls == ["/static/logo.png", "/theme_static/logo.png"]


def test_add_static_files_can_be_found_via_site_map_find(tmp_path):
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "logo.png").write_text("fake-png-bytes")

    sm = SiteMap("http://example.com")
    sm.add_static_files([static_dir])

    found = sm.find("/static/logo.png", attr="url_for")
    assert found is not None
    assert found.title == "logo.png"
    assert sm.find("/static/missing.png", attr="url_for") is None


def test_add_static_files_include_patterns_filters_files(tmp_path):
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "logo.png").write_text("a")
    (static_dir / "notes.txt").write_text("b")

    sm = SiteMap("http://example.com")
    sm.add_static_files([static_dir], include_patterns=["*.png"])

    urls = sorted(entry.url_for for entry in sm)
    assert urls == ["/static/logo.png"]


def test_add_static_files_exclude_patterns_filters_files(tmp_path):
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "logo.png").write_text("a")
    (static_dir / "logo.png.bak").write_text("b")

    sm = SiteMap("http://example.com")
    sm.add_static_files([static_dir], exclude_patterns=["*.bak"])

    urls = sorted(entry.url_for for entry in sm)
    assert urls == ["/static/logo.png"]


def test_add_static_files_exclude_dirs_skips_directory(tmp_path):
    static_dir = tmp_path / "static"
    (static_dir / "drafts").mkdir(parents=True)
    (static_dir / "logo.png").write_text("a")
    (static_dir / "drafts" / "wip.png").write_text("b")

    sm = SiteMap("http://example.com")
    sm.add_static_files([static_dir], exclude_dirs=["drafts"])

    urls = sorted(entry.url_for for entry in sm)
    assert urls == ["/static/logo.png"]


def test_add_static_files_include_dirs_overrides_exclude_dirs(tmp_path):
    static_dir = tmp_path / "static"
    (static_dir / "drafts" / "public").mkdir(parents=True)
    (static_dir / "drafts" / "private").mkdir(parents=True)
    (static_dir / "drafts" / "public" / "notice.png").write_text("a")
    (static_dir / "drafts" / "private" / "secret.png").write_text("b")
    (static_dir / "logo.png").write_text("c")

    sm = SiteMap("http://example.com")
    sm.add_static_files(
        [static_dir],
        exclude_dirs=["drafts"],
        include_dirs=["drafts/public"],
    )

    urls = sorted(entry.url_for for entry in sm)
    assert urls == ["/static/drafts/public/notice.png", "/static/logo.png"]


def test_include_static_in_site_map_false_excludes_from_map(tmp_path):
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "logo.png").write_text("a")

    sm = SiteMap("", {}, static_paths=[static_dir])
    sm.include_static_in_site_map = False
    sm.update({})

    assert list(sm) == []


def test_site_static_filters_apply_through_render(tmp_path_factory):
    base_temp_path = tmp_path_factory.getbasetemp()
    static_dir = base_temp_path / "filtered_static"
    static_dir.mkdir(exist_ok=True)
    (static_dir / "logo.png").write_text("a")
    (static_dir / "notes.txt").write_text("b")
    (static_dir / "drafts").mkdir(exist_ok=True)
    (static_dir / "drafts" / "wip.png").write_text("c")

    tmp_output_path = base_temp_path / "filtered_output"
    tmp_template_path = base_temp_path / "filtered_templates"
    tmp_template_path.mkdir(exist_ok=True)

    class FilteredSite(Site):
        output_path = tmp_output_path
        _template_path = tmp_template_path
        static_paths = {static_dir}
        static_include_patterns = ("*.png",)
        static_exclude_dirs = ("drafts",)
        include_static_in_site_map = True

    filtered_site = FilteredSite()
    filtered_site.render()

    urls = sorted(entry.url_for for entry in filtered_site.site_map if isinstance(entry, StaticSiteMapEntry))
    assert urls == [f"/{static_dir.name}/logo.png"]


def test_include_static_in_site_map_true_includes_in_map(tmp_path):
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "logo.png").write_text("a")

    sm = SiteMap("", {}, static_paths=[static_dir])
    sm.include_static_in_site_map = True
    sm.update({})

    urls = sorted(entry.url_for for entry in sm)
    assert urls == ["/static/logo.png"]
