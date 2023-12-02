import logging
import shutil
import typing

from render_engine.hookspecs import hook_impl
from render_engine.site import Site


class CleanOutput:
    """Clean the output folder before rendering"""

    default_settings = {
        "ignore_errors": False,
    }

    @hook_impl
    def pre_build_site(
        site: Site,
        settings: dict[str, typing.Any] = {
            "CleanOutput": {
                "ignore_errors": True,
            },
        },
    ):
        """Clean the output folder before rendering.

        parameters:
            site: The site object
            settings: The settings for the site
                ignore_errors: If True, ignore errors when removing the output folder
        """
        logging.warning(f"Removing {site.output_path} (if exist) before rendering")
        shutil.rmtree(site.output_path, ignore_errors=settings["CleanOutput"].get("ignore_errors", False))
