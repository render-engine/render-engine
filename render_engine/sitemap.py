"""
The Site Map Generator.

This is the base files and should only contain the params identified by the standards defined.

http://www.sitemaps.org/schemas/sitemap/0.9
"""

import logging
from pathlib import Path

import jinja2
import pendulum
from jinja2 import PackageLoader, select_autoescape
from more_itertools import chunked

from .engine import Engine
from .page import Page


class SiteMapEngine(Engine):
    """
    The Engine that Processes RSS Feed.
    """

    extension = ".xml"
    environment = jinja2.Environment(
        loader=PackageLoader("render_engine", "xml"),
        autoescape=select_autoescape(),
        trim_blocks=True,
    )


def gen_site_map_item(cls):
    """
    The class representation of a sitemap object.

    Note:
            While sitemaps are most commonly used search engine	optimization (SEO).
                    Some fields are deprecated in that usage they will be considered optional.

    Attributes:
            url (str): link to the `Page`. Due to the design of the systems, this uses the
                    reference link and expands to the full link using information from the `Site`.
            lastmod (str): optional, datetime formattted to ISO 8601.
            changefreq (str): optional, one of
                    `always|hourly|daily|monthly|yearly|never`. If any option other than these
                    are provided, the `update_frequency` will not be set.
            priority (float): value between 0.0 and 1.0 to signify priority on the site.
                    Values outside this range will generate a warning on page creation and
                    excluded from the site map.
    """

    return {
        "url": cls.url,
        "lastmod": getattr(cls, "date_published", ""),
        "changefreq": getattr(cls, "sitemap_changefreq", ""),
        "priority": getattr(cls, "sitemap_priority", ""),
    }


def _render_sitemap(segments, output_path, SITE_URL) -> None:
    map_items = [gen_site_map_item(x) for x in segments]
    _segments = list(chunked(map_items, 500000))

    for i, segment in enumerate(_segments):
        _map = SiteMapEngine().get_template("sitemap.xml")
        sitemap_content = _map.render(SITE_URL=SITE_URL, items=segment)
        filename = "sitemap"

        if len(_segments) > 1:
            filename = f"{filename}_{i}.xml"
        else:
            filename = f"{filename}.xml"

        output = Path(output_path / filename)
        output.write_text(sitemap_content)
