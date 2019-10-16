from .blog import Blog
from .collection import Collection
from .engine import Engine
from .page import Page


def route(template_name, content=None, content_path=None, content_type=Page):
    def inner(f, *args, **kwargs):
        func = f(*args, **kwargs)
        p = content_type(content=content, content_path=content_path)
        p.render_template(template_name, **func)

    return inner


def collection(
    template_name, content_path=None, output_path="./", content_type=Collection
):
    def inner(f, *args, **kwargs):
        func = f(*args, **kwargs)
        p = content_type(content_path=None, output_path=output_path)
        p.render_template(template_name, **func)

    return inner
