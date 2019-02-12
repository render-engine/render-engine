import config
import functools

def write_page(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
        return f

def writer(route):
    def write_wrapper(func, route=route):
        def wrapper(*args, **kwargs):
           page = write_page(f'{config.OUTPUT_PATH}/{route}', func(*args, **kwargs))
        return wrapper
    return write_wrapper
