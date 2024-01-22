from render_engine_tailwindcss import TailwindCSS

from render_engine import Collection, Page, Site
from render_engine.parsers.markdown import MarkdownPageParser
from render_engine_pagefind import PageFind

if True: print("hello") # noqa

site = Site()
SITE_TITLE = "Render Engine"
SITE_URL = "https://render-engine.readthedocs.io/"
site.site_settings.update({
    "site_title": SITE_TITLE,
    "site_url": SITE_URL,
})

site.register_plugins(TailwindCSS)
site.output_path = "docs/output"
site.register_themes(PageFind)

@site.collection
class Getting_Started(Collection):
    routes = ["getting-started"]
    content_path = "/Users/kjaymiller/render-engine/docs/docs/getting-started/"
    Parser = MarkdownPageParser

@site.collection
class Contributing(Collection):
    routes = ["contributing"]
    content_path = "/Users/kjaymiller/render-engine/docs/docs/getting-started/"
    Parser = MarkdownPageParser

@site.page
class Index(Page):
    content_path = "README.md"
    Parser = MarkdownPageParser