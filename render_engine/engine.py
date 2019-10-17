import logging
import os
import shutil
from pathlib import Path
from typing import Optional, Sequence, Type
from .helpers import PathString

from jinja2 import FileSystemLoader, select_autoescape
import jinja2

from render_engine.page import Page

# Currently all of the Configuration Information is saved to Default
logging.basicConfig(level=os.environ.get("LOGGING_LEVEL", logging.WARNING))


class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""

    def __init__(
        self,
        content_type: Type[Page],
        output_path: PathString = Path("output"),
        # Jinja2.FileSystemLoader takes str or iterable not Path
        templates_path: str = "templates",
        extension: str = ".html",
        autoescape: Sequence = ["html"],
    ):

        self.environment = jinja2.Environment(
                loader=FileSystemLoader(templates_path),
                autoescape=select_autoescape(autoescape),
            )

        self.content_type = content_type
