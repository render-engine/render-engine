import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

from render_engine._base_object import BaseObject
from render_engine.plugins import PluginManager


class DataObject(BaseObject):
    """Class to store a data object"""

    data_object: Any = None  # The data object
    serializer: Callable
    serializer_args: dict = {}

    routes: list[str | Path] = ["./"]
    path_name: str | Path = Path("data_object.json")
    plugin_manager: PluginManager | None
    site = None  # This is a Site but circular imports so we can't actually type hint it.

    def __init__(self, serializer: Callable = json.dumps):
        """Ensure that the serializer method is static"""
        self.serializer = staticmethod(serializer)

    @property
    def filename(self) -> str:
        if not isinstance(self.path_name, Path):
            self.path_name = Path(self.path_name)
        return self.path_name.name

    def render(self, *args, **kwargs):
        """
        Renders the data_object to the file at output_file
        """
        from .site import Site

        site: Site = cast(Site, self.site)
        for route in self.routes:
            path = Path(site.output_path, route, self.path_name)
            path.parent.mkdir(parents=True, exist_ok=True)

            settings = dict()
            if (pm := getattr(self, "plugin_manager", None)) and pm is not None:
                settings = {**site.plugin_manager.plugin_settings, "route": self.path_name}
                pm.hook.render_content(page=self, settings=settings, site=self.site)

            data_object = self.data_object
            serialized = (
                self.serializer(data_object, **self.serializer_args)
                if self.serializer_args
                else self.serializer(self.data_object)
            )

            if pm is not None:
                pm.hook.post_render_content(page=self.__class__, settings=settings, site=self.site)

            path.write_text(serialized)
