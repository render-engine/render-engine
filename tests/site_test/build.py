from render_engine.page import Page
from render_engine.site import Site

app = Site()


class Base_Page(Page):
    content = "this is a test testing the Base Page"
