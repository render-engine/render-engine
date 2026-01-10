from pathlib import Path

from render_engine import Collection
from render_engine.content_managers import FileContentManager


def test_find_entry(tmp_path):
    content_path = Path(tmp_path, "test-collection")
    content_path.mkdir(parents=True)
    filepath = content_path / "content.md"
    content = "Test new content"
    filepath.write_text(content)

    class TestCollection(Collection):
        content_path = Path(tmp_path, "test-collection")
        ContentManager = FileContentManager

    collection = TestCollection()
    page = collection.content_manager.find_entry(content_path=filepath)
    assert page is not None
    assert page.content_path == filepath
    assert page.content == content


def test_find_no_valid_entry(tmp_path):
    content_path = Path(tmp_path, "test-collection")
    content_path.mkdir(parents=True)
    filepath = content_path / "content.md"
    content = "Test new content"
    filepath.write_text(content)

    class TestCollection(Collection):
        content_path = Path(tmp_path, "test-collection")
        ContentManager = FileContentManager

    collection = TestCollection()
    page = collection.content_manager.find_entry(content_path=filepath, test_attr="Test")
    assert page is None
    page = collection.content_manager.find_entry(content_path=filepath)
    assert page is not None


def test_find_entry_no_entries(tmp_path):
    content_path = Path(tmp_path, "test-collection")
    content_path.mkdir(parents=True)
    filepath = content_path / "content.md"

    class TestCollection(Collection):
        content_path = Path(tmp_path, "test-collection")
        ContentManager = FileContentManager

    collection = TestCollection()
    page = collection.content_manager.find_entry(content_path=filepath)
    assert page is None


def test_update_entry(tmp_path):
    content_path = Path(tmp_path, "test-collection")
    content_path.mkdir(parents=True)
    filepath = content_path / "content.md"
    content = "Test new content"
    updated = "Test updated content"
    filepath.write_text(content)

    class TestCollection(Collection):
        content_path = Path(tmp_path, "test-collection")
        ContentManager = FileContentManager

    collection = TestCollection()
    assert len(collection.content_manager) == 1
    page = collection.content_manager.find_entry(content_path=filepath)
    assert filepath.read_text() == page.content
    collection.content_manager.update_entry(page, content=updated, test_attr="Test")
    assert filepath.read_text() == f"---\ntest_attr: Test\n---\n\n{updated}"
    page = collection.content_manager.find_entry(content_path=filepath)
    assert page.content == updated
    assert page.test_attr == "Test"
    assert len(collection.content_manager) == 1
