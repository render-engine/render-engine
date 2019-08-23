from render_engine import Page


def test_can_create_Page():
    assert Page(slug='base_page')
