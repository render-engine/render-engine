import json
import logging


class Search:
    def __init__(self, name):
        self.name = name

    def build_index(self, pages, keys, filepath):
        search_index = []

        for page in pages:
            logging.debug(f"{page=}")

            if keys:
                search_index.append(
                    {x: str(y) for x, y in vars(page).items() if x in keys}
                )

            else:
                logging.debug(vars(page))
                search_index.append({x: str(y) for x, y in vars(page).items()})

        with open(filepath, 'w') as jsonfile:
            return json.dump(search_index, fp=jsonfile)


Fuse = Search("fuse")
