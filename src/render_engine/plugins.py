import pluggy

from .hookspecs import _PROJECT_NAME, SiteSpecs


class PluginManager:
    _pm: pluggy.PluginManager

    def __init__(self, PluginManagers: list[pluggy.PluginManager]):
        """Create a new PluginManager"""

        self._pm = pluggy.PluginManager(project_name=_PROJECT_NAME)
        self._pm.add_hookspecs(SiteSpecs)
        
        for PluginManager in PluginManagers:
            self.register(PluginManager)
            
            for PluginManager in PluginManagers:
                self._pm.get_plugins
                self._pm.register(PluginManager)

    
    def register_plugins(self, *plugins, **settings: dict[str, typing.Any]) -> None:
        """Register plugins with the site

        parameters:
            plugins: list of plugins to register
            settings: settings to pass into the plugins
                settings keys are the plugin names as strings.
        """

        for plugin in plugins:
            self._pm.register(plugin)
            self.site_settings["plugins"][plugin.__name__] = getattr(plugin, "default_settings", {})

        self._pm.hook.add_default_settings(
            site=self,
            custom_settings=settings,
        )

        self.site_settings["plugins"].update(**settings)

    @property
    def plugins(self):
        return self._pm.get_plugins()



