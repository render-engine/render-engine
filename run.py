import generators
def run(overwrite=True):
    return gen_static(static_path=config.STATIC_PATH, overwrite=overwrite)
