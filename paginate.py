def write_paginated_pages(name, pagination, *, route, content_type, **kwargs):
    p_routes = []
    for block in enumerate(pagination):
        block_route = f'{route}/{name}_{block[0]}'
        kwargs['post_list'] = [b for b in filter(lambda x:x, block[1])]

        page = content_type(
                    template=kwargs.get('template', 'archive.html'),
                    route=block_route,
                    post_list=[x for x in list(filter(lambda x:x, block[1]))],
                    )
        p_routes.append(page)

    return p_routes
