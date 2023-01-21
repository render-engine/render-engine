"""
Plugins are a way to extend the functionality of the render engine site.
"""

import pathlib
import shutil

from render_engine.engine import engine
from render_engine.hookspecs import hook_impl


class Clean:
    """Clean the output folder before rendering"""

    @hook_impl
    def pre_site_build(site: Site):
        """Clean the output folder before rendering"""
        shutil.rmtree(site.output_path, ignore_errors=True)


class SiteMap:
    """Generate a sitemap.xml file"""

    @hook_impl
    def post_site_build(site: Site):
        """Generate a sitemap.xml file"""
        template = engine.get_template("sitemap.xml")
        template.render(
            items=pathlib.Path(site.output_path).iterdir(),
        )
