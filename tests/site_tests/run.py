from render_engine import Engine

engine = Engine()

# Build a basic page with no Template
from render_engine.page import Page
index = Page(
        slug='/index', # Don't Include '/'
        content="""<html>
        <body><h1>This is a Sample Page</h1></body>
        </html>"""
        )

engine.routes.append(index)
engine.run()
