from render_engine.site import Site
from render_engine.page import Page
from render_engine.engine import Engine
from render_engine.collection import Collection
from render_engine.blog import Blog


app = Site()

class Base_Page(Page):
    content = "this is a test testing the Base Page"

