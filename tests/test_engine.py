from jinja2 import Markup
from pathlib import Path
from render_engine import Engine, Page
import pytest

@pytest.mark.skip()
def test_engine(tmpdir):
    p = tmpdir.mkdir('templates')
    pf = p.join('test_file')
    pf.write('This is a Test')

    class TestEngine(Engine):
        template_path = p.strpath

    te = TestEngine()

    print(te.environment)
    assert TestEngine().get_template('This is a Test').render() == 'This is a Test'
