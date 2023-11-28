import logging
import pathlib
import typing

from render_engine.engine import engine
from render_engine.hookspecs import hook_impl
from render_engine.site import Site


class SiteMap:
    """Generate a sitemap.xml file"""

    default_settings = {
        "template": "sitemap.xml",
        "output_path": "sitemap.xml",
        "map_item_pattern": "*.html",
    }

    @hook_impl
    def post_build_site(
        site: Site,
        settings: dict[str, typing.Any],
    ):
        """Generate a sitemap.xml file.

        parameters:
            site: The site object
            settings: The settings for the site
                template: The template to use for the sitemap.xml file
                output_path: The path to the sitemap.xml file. output_path is relative to the output_path of the site
                map_item_pattern: The pattern to use to find the files to include in the sitemap.xml file
        """
        logging.info(
            f"""Generating sitemap - {settings['SiteMap']['output_path']}
                     from files matching - {settings['SiteMap']['map_item_pattern']}
                     using template - {settings['SiteMap']['template']}"""
        )
        template = engine.get_template(settings["SiteMap"]["template"])
        site_map_items = pathlib.Path(site.output_path).rglob(settings["SiteMap"]["map_item_pattern"])
        sitemap_path = pathlib.Path(site.output_path).joinpath(settings["SiteMap"]["output_path"])
        sitemap_path.write_text(
            template.render(
                items=[item.relative_to(site.output_path) for item in site_map_items],
            )
        )
