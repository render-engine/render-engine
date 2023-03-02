from render_engine._base_object import BaseObject

class TestObject(BaseObject):
    pass
    

class TestBaseObjectProperties:

    test_object = TestObject()

    def test_base_object__title_defaults_to_class_name(self):
        """assert that the title defaults to the class name"""

        assert self.test_object._title == "TestObject"


    def test_base_object__slug_defaults_to_title(self):
        """assert that the slug defaults to a slugified title"""
        assert self.test_object._slug == "testobject"


    def test_base_object__extension_defaults_to_html(self):
        """
        asserts that the extension defaults to .html
        This is to assure that is a page is generated from any object
        it will have a valid extension.
        """

        assert self.test_object.extension == ".html"

    def test_base_object__extension_starts_with_dot(self):
        """
        asserts that the extension starts with a dot
        This is to assure that is a page is generated from any object
        """
        
        no_dot_BaseObject = BaseObject()
        no_dot_BaseObject.extension = "xml"
        assert self.test_object.extension.startswith(".")