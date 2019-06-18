from generators import gen_static
from base_config import config

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""

    # Currently all of the Configuration Information is saved to Default
    config = config['DEFAULT']

    def __init__(self, *, conent_path, output_path):
        self.conent_path = content_path
        self.output_path = output_path

    def build(self, collections):
        static_pages = gen_static(
            static_path=STATIC_PATH,
            overwrite=overwrite,
            )

        for collection in collections:
            collection.output_path.mkdir(
            parents=True,
            exist_ok=True,
            )

    def run(self, overwrite=True):
        for page in self.collections:
            write_page(
            f'{collection.output_path}/{page.id}.html',
        page.html)

