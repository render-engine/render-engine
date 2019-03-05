import json

def feed_gen(collection, output_path=None, name=None):
    output_path = output_path or collection.output_path
    name = name or collection.name

    with open(f'{output_path}/{name}.json', 'w') as fp:
        json.dump(collection.json_feed, fp)

    with open(f'{output_path}/{name}.rss', 'w') as rss:
        rss.write(collection.rss_feed)
