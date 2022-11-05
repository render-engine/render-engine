import pytest
from jinja2 import Template

from render_engine.collection import Collection


@pytest.fixture(scope="session")
def temp_dir_collection(gen_content, tmp_path_factory):
    tpd = tmp_path_factory.mktemp("test_collection")
    for n in range(5):
        fake_path = tpd / f"fake_path_{n}.md"
        fake_path.write_text(f"{gen_content} {n}", encoding="utf-8")

    yield tpd


@pytest.fixture(scope="session")
def base_collection(temp_dir_collection):
    class MyCollection(Collection):
        content_path = temp_dir_collection
        list_attrs = "custom_list"
        archive_template = Template("Foo")

    yield MyCollection()


@pytest.fixture(scope="session")
def custom_collection(temp_dir_collection):
    class CustomCollection(Collection):
        content_path = temp_dir_collection
        title = "My Custom Title"
        foo = "bar"
        items_per_page = 2

    yield CustomCollection()
