from generators import gen_static
from .config import STATIC_PATH

def run(overwrite=True):
    return gen_static(static_path=STATIC_PATH, overwrite=overwrite)
