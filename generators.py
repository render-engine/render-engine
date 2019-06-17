"""
Generates the files to build out your HTML Path
"""
import shutil
from pathlib import Path

# from render_engine.feeds import PathCrawler
import config

def remove_path(path):
    # Remove output directory if it exists
    try:
        shutil.rmtree(path.output_path)
    except:
        pass

def gen_static(static_path: str='static', overwrite: bool=True):
    path = Path(f'{config.OUTPUT_PATH}/{static_path}')
    if overwrite:
        shutil.rmtree(static_path)

    return shutil.copytree(static_path, path)
