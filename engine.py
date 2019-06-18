from collection import Collection
from pathlib import Path
from base_config import config


config = config['DEFAULT']

class Engine:
    def __init__(self,
            collections: list=[],
            ):

        # use configparser to load the base config file
        # overwrite it with the file at `config_path`
        # config files can have any extension but probably shouldn't
        self.collections = collections


    def run(overwrite=True):
        for collection in self.collections:
            collection.output_path.mkdir(parents=True, exist_ok=True)

            for page in collection.pages:
                output_path = f'{collection.output_path}/{page.id}.html'
                write_page(output_path, page.html)

        gen_static(
                static_path=config['STATIC_PATH'],
                overwrite=overwrite
                )


if __name__ == '__main__':
    engine = Engine()
