import typing
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, Template

from render_engine.page import Page


@pytest.fixture(scope="session")
def content(gen_content):
    return gen_content


@pytest.fixture(scope="session")
def base_content():
    return """<h1>Test Header</h1>

<p>Test Paragraph</p>

<p><code>&lt;p&gt;Raw HTML&lt;/p&gt;</code></p>
"""


@pytest.fixture(scope="session")
def gen_content(n: typing.Optional[int] = None):
    if not n:
        n = ""
    return f"""---
title: Test Title {n}
custom_list: foo, bar, biz
custom_attr: this is an attribute
---

# Test Header {n}

Test Paragraph

`<p>Raw HTML</p>`"""


@pytest.fixture(scope="session")
def temp_path(tmp_path_factory):
    yield tmp_path_factory.mktemp("test_dir")


@pytest.fixture(scope="class", name="basic_page")
def base_page():
    """Tests can a simple Page be created given no Parameters"""

    class BasePage(Page):
        pass

    yield BasePage()


@pytest.fixture(scope="module", name="p_attrs")
def page_with_attrs():
    """Supply this page objects with attributes"""

    class PageWithAttrs(Page):
        title = "Page with Attrs"
        slug = "Page Slug with Attrs"  # invalid slug format but should be caught
        markdown = """# Test Header
Test Paragraph"""
        custom_list = ["foo", "bar", "biz"]
        custom_attr = "this is an attribute"
        template = Template("{{content}}")

    yield PageWithAttrs()


@pytest.fixture(scope="class", name="with_path")
def page_with_content_path(temp_path, gen_content):
    fake_path = Path(temp_path / "fake_path.md")
    fake_path.write_text(gen_content)

    class PageWithContentPath(Page):
        content_path = fake_path
        list_attrs = "custom_list"

    yield PageWithContentPath()


@pytest.fixture(scope="class", name="no_template")
def render_page_no_template(temp_path, p_attrs):
    engine = Environment(loader=FileSystemLoader(["templates"]))
    p_attrs.render(engine=engine, path=temp_path)
    check_path = Path(temp_path / f"{p_attrs.slug}{p_attrs.extension}")
    yield check_path


@pytest.fixture(scope="class", name="with_template")
def render_page_template(temp_path, p_attrs):
    engine = Environment(loader=FileSystemLoader(["templates"]))
    p_attrs.render(engine=engine, path=temp_path)
    check_path = Path(temp_path / f"{p_attrs.slug}{p_attrs._extension}")
    yield check_path
