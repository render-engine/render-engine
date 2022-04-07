from pathlib import Path
import pytest
from render_engine import Page
from jinja2 import Template

@pytest.fixture(scope='session')
def content():
   yield """
---   
title: Test Title
custom_list: foo, bar, biz
custom_attr: this is an attribute
---

# Test Header

Test Paragraph

`<p>Raw HTML</p>`"""


@pytest.fixture(scope='session')
def temp_dir(tmpdir_factory):
    yield tmpdir_factory.mktemp('test_dir')

@pytest.fixture(scope='class', name='page')
def base_page():
    """Tests can a simple Page be created given no Parameters"""
    class BasePage(Page):
        pass

    yield BasePage()

@pytest.fixture(scope='module', name='p_attrs')
def page_with_attrs():
    """Supply this page objects with attributes"""

    class PageWithAttrs(Page):
        title = 'Page with Attrs'
        slug = 'Page Slug with Attrs' # invalid slug format but should be caught
        markdown = """# Test Header
Test Paragraph"""
        custom_list = ['foo', 'bar', 'biz']
        custom_attr = "this is an attribute"

    yield PageWithAttrs()


@pytest.fixture(scope='class', name='with_path')
def page_with_content_path(temp_dir, content):
    fake_path = Path(temp_dir / 'fake_path.md')
    fake_path.write_text(content)

    class PageWithContentPath(Page):
        content_path = fake_path
        list_attrs = 'custom_list'

    yield PageWithContentPath()


@pytest.fixture(scope='class', name='no_template')
def render_page_no_template(temp_dir, p_attrs):
        p_attrs.render(output_path = temp_dir)
        check_path =  Path(temp_dir / f"{p_attrs.slug}{p_attrs.extension}")
        yield check_path
    

@pytest.fixture(scope='class', name='with_template')
def render_page_template(temp_dir, p_attrs):
        p_attrs.render(output_path = temp_dir, template=Template('foo{{content}}'))
        check_path =  Path(temp_dir / f"{p_attrs.slug}{p_attrs.extension}")
        yield check_path