from itertools import zip_longest
from environment import env
from writer import write_page
import config

def paginate(iterable, items_per_page, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * items_per_page
    iterable = zip_longest(*args, fillvalue=fillvalue) 
    return iterable

def write_paginated_pages(name, pagination, template, path, **kwargs):
    temp =  env.get_template(template)
    for block in enumerate(pagination):
        render = temp.render(post_list=[b for b in block[1] if b], config=config, **kwargs)
        write_page(f'{path}/{name}_{block[0]}.html', render)
