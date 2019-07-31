import pytest
from page import Page

def test_Page_creation():
    """Tests can a simple Page be created given no Parameters"""
    assert Page(route='/test.html')
