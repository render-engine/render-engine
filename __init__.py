from .page import Page
from .blog import BlogPost
from .microblog import MicroBlogPost
from .collection import Collection
from .environment import env

class Engine:
    def run(overwrite=True):
        return gen_static(
                static_path=STATIC_PATH,
                overwrite=overwrite
                )
