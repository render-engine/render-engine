import importlib
import warnings


def test_deperecated_warning():
    with warnings.catch_warnings(record=True) as w:
        importlib.import_module("render_engine.parsers.markdown")
        assert any(isinstance(i.message, DeprecationWarning) for i in w)
