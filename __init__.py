from .page import Page
from .blog import BlogPost
from .microblog import MicroBlogPost
from .collection import Collection
from .environment import env

class Engine:
    def __init__(self, collections):
        self.collections = collections

    def run(overwrite=True):
        for collection in self.collections:
            collection.output_path.mkdir(parents=True, exist_ok=True)

            for page in collection.pages:
                write_page(f'{collection.output_path}/{page.id}.html', page.html)

        return gen_static(
                static_path=STATIC_PATH,
                overwrite=overwrite
                )
