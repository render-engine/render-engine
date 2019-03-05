import json

def feed_gen(collection, page_filter=None, output_path=None, name=None):
    output_path = output_path or collection.output_path
    name = name or collection.name

    with open(f'{output_path}/{name}.json', 'w') as fp:
        json.dump(collection.generate_from_metadata(pages=page_filter), fp)

    with open(f'{output_path}/{name}.rss', 'w') as rss:
        rss.write(collection.generate_rss_feed(pages=page_filter))
