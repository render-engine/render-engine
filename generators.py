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

def gen_static(static_path: Path, overwrite: bool=True):
    if overwrite:
        shutil.rmtree(Path(

    return shutil.copytree(static_path, Path(f'{config.OUTPUT_PATH}/static'))
