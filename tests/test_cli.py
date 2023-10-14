from pathlib import Path

def test_cli_author_name(cli, tmp_path_factory):
    """Asserts there is a SITE_AUTHOR and SITE_EMAIL in the author patch"""
    temp_app = tmp_path_factory.getbasetemp() / "test_app" / "app.py"
    assert "\"name\": \"Test Site Author\"" in temp_app.read_text()

def test_cli_author_email(cli, tmp_path_factory):
    """Asserts there is a SITE_AUTHOR and SITE_EMAIL in the author patch"""
    temp_app = tmp_path_factory.getbasetemp() / "test_app" / "app.py"
    assert "\"email\": \me@example.com"