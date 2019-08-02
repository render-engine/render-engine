from pathlib import Path
import yaml

def created_message(path):
    return f'{path} created!'

def skip_message(path):
    return f'{path} exists! Skipping...'

def main(
        template_path='templates',
        content_path='content',
        config_path='config.yaml',
        **kwargs,
        ):
    template_path = Path(template_path)
    content_path = Path(content_path)
    config_path = Path(config_path)

    if not config_path.exists():
        config_path.write_text(
            yaml.dump({'engine_variables': {
                    'content_path': content_path,
                    'template_path': template_path,
                    }})
            )
        print(created_message(config_path))

    else:
        print(skip_message(config_path))

    for path in (template_path, content_path):
        if not path.is_dir():
            Path(path).mkdir(exist_ok=True, **kwargs)
            print(created_message(path))

        else:
            print(skip_message(str(path)))

if __name__ == '__main__':
    main()
