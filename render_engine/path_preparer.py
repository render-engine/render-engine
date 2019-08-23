def directory_path(path, base_path='./'):
    base_path = Path(base_path)
    return base_path.joinpath(path)
