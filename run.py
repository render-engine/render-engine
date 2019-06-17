from generators import gen_static

def run(overwrite=True):
    return gen_static(static_path=config.STATIC_PATH, overwrite=overwrite)
