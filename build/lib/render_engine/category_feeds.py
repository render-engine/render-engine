    title = _[1].capitalize()
    with open(f'{_[0]}/{_[1]}_feed.json', 'w') as f:
        json.dump(json_feed(items=_[0]['pages'],
                path=output_path,
                title=), _[0]['output_path'])
