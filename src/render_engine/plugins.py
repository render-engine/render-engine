"""
Plugins are a way to extend the functionality of the render engine site.
"""

import pathlib
import shutil

from render_engine.engine import engine
from render_engine.hookspecs import hook_impl
from render_engine.site import Site


class CleanOutput:
    """Clean the output folder before rendering"""

    @hook_impl
    def pre_build_site(site: type[Site]):
        """Clean the output folder before rendering"""
        print(f"Removing {site.output_path} (if exist) before rendering")
        shutil.rmtree(site.output_path, ignore_errors=True)


class SiteMap:
    """Generate a sitemap.xml file"""

    @hook_impl
    def post_build_site(site: type[Site]):
        """Generate a sitemap.xml file"""
        print("Generating sitemap.xml")
        template = engine.get_template("sitemap.xml")
        site_map_items = pathlib.Path(site.output_path).rglob("*.html")
        sitemap_path = pathlib.Path(site.output_path).joinpath("sitemap.xml")
        sitemap_path.write_text(
            template.render(
                items=[item.relative_to(site.output_path) for item in site_map_items],
            )
        )
