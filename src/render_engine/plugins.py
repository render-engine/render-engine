import pluggy

from .hookspecs import _PROJECT_NAME, SiteSpecs


class PluginManager:
    def __init__(self):
        self._pm = pluggy.PluginManager(project_name=_PROJECT_NAME)
        self._pm.add_hookspecs(SiteSpecs)

    def register_plugin(self, plugin) -> None:
        """Register a plugin with the site"""
        self._pm.register(plugin)

    @property
    def plugins(self):
        return self._pm.get_plugins()
