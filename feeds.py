def feed_gen(collection):
    with open(f'{collection.output_path}/{collection.name}.json', 'w') as fp:
        json.dump(collection.json_feed, fp)

    with open(f'{collection.output_path}/{collection.name}.rss', 'w') as rss:
        rss.write(collection.rss_feed)
