from pathlib import Path
from .base_config import config
import shutil

# Currently all of the Configuration Information is saved to Default
config = config['DEFAULT']
content_path='content'
output_path='output'
static_path='static'

def paginate(iterable, items_per_page, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * items_per_page
    iterable = zip_longest(*args, fillvalue=fillvalue)
    return iterable


def write_paginated_pages(name, pagination, template, path, **kwargs):
    temp =  env.get_template(template)
    for block in enumerate(pagination):
        render = temp.render(
                post_list=[b for b in block[1] if b],
                config=config,
                **kwargs,
                )
        write_page(f'{path}/{name}_{block[0]}.html', render)


class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""
    content_path = Path(content_path)
    output_path = Path(output_path)
    static_path = Path(static_path)
    routes_index = dict()

    def add_route(self,
            content_type,
            *,
            template,
            route='',
            routes=[],
            base_file=None,
            **kwargs,
            ):
        """Used to Create the HTML that will be added to Routes. Usually not
        called on it's own."""

        content = content_type(
                template=template,
                base_file=base_file,
                **kwargs,
                )

        if content.id:
            route += f'/{content.id}'

        if route:
            routes.append(route)

        return (self.route_index[f'{r}'] = content.html for r in routes)

    def build(self, content_type, *, template, route='', routes=[], base_file=None):
        """Used to get **kwargs for `add_route`"""

        def inner(func):
            kwargs = func() or {}
            self.add_route(
                    content_type,
                    route=route,
                    routes=routes,
                    template=template,
                    **kwargs
                    )
            return func

        return inner

    def add_collection(
            self,
            content_type,
            *,
            template,
            content_path,
            route='',
            routes=[],
            paginate=True,
            feed=True,
            feed_template=None,
            extension='.md',
            **kwargs,
            ):

        """Iterate through the provided content path building the desired
        content_type and storing in routes to be created on run"""
        content_path = Path(content_path)

        collection_items = content_path.glob(f'*{extension}')

        if route:
            routes.append(route)

        return (sef.add_route(
                    content_type,
                    template=template,
                    route = x+y,
                    base_file=path,
                    **kwargs) for x in routes for y in collection_items)

    def run(self, overwrite=True):
        """Builds the Site Objects
        1. Generate Static Pages
        2. Generate Collections
        3. Generate Custom Pages

        TODO: Add Skips to ByPass Certain Steps
        """

        static_output = f"{self.output_path}/{self.static_path}"

        # If overwrite AND THE FILE EXISTS, then remove the entire folder
        if all((overwrite, Path(self.output_path).exists())):
            shutil.rmtree(self.output_path)
            Path(self.output_path).mkdir() # Creates the new folder

        # Instead of trying to analyze the static folder. Just delete the
        # contents
        try:
            shutil.rmtree(static_output)
        except:
            pass

        shutil.copytree(
            self.static_path,
            static_output,
            )

        for path, content in self.routes_index.items():
            filename = Path(f'{self.output_path}/{path}.html').resolve()
            base_dir = filename.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                    )

            if filename.exists():
                with filename.open() as f:
                    if f.read() == content:
                        continue

                    else:
                        filename.unlink()

            with filename.open('w') as f:
                f.write(content)
