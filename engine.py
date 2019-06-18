from pathlib import Path
from .base_config import config
import shutil

# Currently all of the Configuration Information is saved to Default
config = config['DEFAULT']

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""
    def __init__(
            self,
            *,
            content_path='content',
            output_path='output',
            static_path='static',
            ):
        self.content_path = Path(content_path)
        self.output_path = Path(output_path)
        self.static_path = Path(static_path)
        self.collections = []
        self.routes = dict()

        # Remove output directory if it exists
        try:
            shutil.rmtree(self.output_path)

        except:
            pass

    def build(self, content_type, *, template, route):
        def inner(func):
            r = func
            content = content_type(template=template).html
            self.routes[f'{route}.html'] = content

            return r
        return inner


        self.pages.append(new_page)

    def collection(self, paginate=True, feed=True, feed_template=None):
        def inner(func):
            return funct

        return inner


    def run(self, overwrite=True):
        """Builds the Site Objects
        1. Generate Static Pages
        2. Generate Collections
        3. Generate Custom Pages

        TODO: Add Skips to ByPass Certain Steps
        """

        shutil.copytree(
            self.static_path,
            f"{config['OUTPUT_PATH']}/{config['STATIC_PATH']}",
            )

        for collection in self.collections:
            Path(config['OUTPUT_PATH']).joinpath(
                    collection.output_path).mkdir(
                    parents=True,
                    exist_ok=True,
                    )

            for page in collection.pages:
                route = f'{collection.output_path}/{page.id}.html'
                content = page.html
                self.routes[route] = content


        for page in self.routes:
            filename = f'{self.output_path}/{page}'
            with open(filename, 'w') as f:
                print(filename + ' has been added')
                f.write(self.routes[page])

