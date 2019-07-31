def write_paginated_pages(name, pagination, *, route, content_type, **kwargs):
    p_routes = []
    for index, block in enumerate(pagination):
            block_route = f'{route}/{name}_{index}'
            post_list = list(filter(lambda x:x[1], enumerate(block)))
            page = content_type(
                    template=kwargs.get('template', 'archive.html'),
                    route=block_route,
                    post_list=post_list,
                    )
            p_routes.append(page)
    return p_routes
