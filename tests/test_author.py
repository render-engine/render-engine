import pytest
from render_engine.author import Author


def test_Author_email_and_name_as_string_has_format():
    name = 'John Doe'
    email = 'johnd@example.com'
    name_string = f'{email} ({name})'

    author = Author(email=email, name=name)
    assert str(author) == name_string

def test_Author_with_no_name_as_string_is_email():
    email = 'johnd@example.com'
    author = Author(email=email)
    assert str(author) == email

def test_Author_must_have_email():
    with pytest.raises(TypeError):
        Author()
