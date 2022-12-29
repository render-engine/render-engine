from jinja2 import ChoiceLoader, PackageLoader

render_engine_templates_loader = ChoiceLoader(
    [
        PackageLoader("render_engine", "render_engine_templates"),
    ]
)
