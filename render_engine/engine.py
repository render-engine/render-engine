from render_engine.collection import Collection
from itertools import zip_longest
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from typing import Type, Optional, Union, TypeVar

import logging
import os
import shutil
import yaml

# Currently all of the Configuration Information is saved to Default
logging.basicConfig(level=os.environ.get('LOGGING_LEVEL', logging.WARNING))

PathString = Union[str, Type[Path]]

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""

    def __init__(self,
            output_path:PathString=Path('output'),
            static_path:PathString=Path('static'),
            strict: bool=False,
            env_variables: dict={},
            templates_dir: PathString=Path('templates'),
            ):

        self.output_path = Path(output_path)

        if strict:
                shutil.rmtree(self.output_path)

        if not self.output_path.is_dir():
            self.output_path.mkdir(exist_ok=True)

        self.static_path = Path(static_path)
        if self.static_path.is_dir():
            output_static_path = self.output_path.joinpath(self.static_path)

            if output_static_path.exists():
                shutil.rmtree(output_static_path)
                shutil.copytree(src=static_path, dst=output_static_path)
