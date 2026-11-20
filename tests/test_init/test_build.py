"""End-to-end tests: generated sites must build.

These tests create a site from the built-in template and build it by running its app file
in a separate process, the way a user would. They catch problems the other tests can't,
like a wrong import in the generated app file or a template that doesn't exist.

They are slower than the other tests, so they cover the main combinations of answers
rather than every case.
"""

import subprocess
import sys

import pytest

from render_engine.init import InitOptions, create_site


def build(site_path, options):
    """Build a generated site the way a user would: by running its app file."""
    return subprocess.run(
        [sys.executable, options.app_filename],
        cwd=site_path,
        capture_output=True,
        text=True,
        timeout=60,
    )


@pytest.mark.parametrize("include_collection", [True, False])
@pytest.mark.parametrize("include_blog", [True, False])
def test_generated_site_builds(tmp_path, include_blog, include_collection):
    options = InitOptions(site_title="My Blog", include_blog=include_blog, include_collection=include_collection)
    site_path = create_site(options, tmp_path)

    result = build(site_path, options)

    assert result.returncode == 0, result.stderr
    output = site_path / "output"
    assert "My Blog" in (output / "index.html").read_text(encoding="utf-8")
    assert (output / "static" / "style.css").is_file()
    assert (output / "blog" / "example-blog-post.html").exists() is include_blog
    assert (output / "example-page.html").exists() is include_collection


def test_generated_site_builds_with_custom_names(tmp_path):
    options = InitOptions(site_title="Cool website", app_filename="my-site.py", output_path="public")
    site_path = create_site(options, tmp_path)

    result = build(site_path, options)

    assert result.returncode == 0, result.stderr
    assert "Cool website" in (site_path / "public" / "index.html").read_text(encoding="utf-8")


def test_site_title_is_escaped_in_html(tmp_path):
    options = InitOptions(site_title="Tom & Jerry <Fan Club>")
    site_path = create_site(options, tmp_path)

    result = build(site_path, options)

    assert result.returncode == 0, result.stderr
    html = (site_path / "output" / "index.html").read_text(encoding="utf-8")
    assert "<h1>Tom &amp; Jerry &lt;Fan Club&gt;</h1>" in html
    assert '<a href="https://example.com">' in html
