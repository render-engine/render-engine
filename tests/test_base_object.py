from render_engine._base_object import BaseObject


class TestObject(BaseObject):
    pass


class TestBaseObjectProperties:
    test_object = TestObject()

    def test_base_object__title_defaults_to_class_name(self):
        """assert that the title defaults to the class name"""

        assert self.test_object._title == "TestObject"

    def test_base_object_plugin_settings_defaults_to_plugins_dict(self):
        """assert that the plugin_settings defaults to plugins dict"""

        assert self.test_object.plugin_settings == {"plugins": {}}

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
        assert no_dot_BaseObject.extension == ".xml"

    def test_base_object_path_name(self):
        """Tests that the path name is returned correctly"""
        assert self.test_object.path_name == "testobject.html"

    def test_base_object_to_dict(self):
        """Tests that the to_dict method returns a dict of the object's attributes"""
        assert self.test_object.to_dict() == {
            "title": "TestObject",
            "slug": "testobject",
            "url": None,
            "path_name": "testobject.html",
            "plugins": {},
        }

    def test_base_object_to_dict_with_template_vars(self):
        """Tests that the `to_dict` adds template_vars extracted method returns a dict of the object's attributes"""
        self.test_object.template_vars = {"test": "test"}
        self.test_object.plugin_settings = {"plugins": {"test_plugin": "test"}}

        assert self.test_object.to_dict() == {
            "title": "TestObject",
            "slug": "testobject",
            "url": None,
            "test": "test",
            "template_vars": {"test": "test"},
            "path_name": "testobject.html",
            "plugin_settings": {"plugins": {"test_plugin": "test"}},
            "plugins": {"test_plugin": "test"},
        }

        assert self.test_object.template_vars == {"test": "test"}
        assert self.test_object.plugin_settings == {"plugins": {"test_plugin": "test"}}


def test_base_object():
    assert BaseObject._metadata_attrs()["title"] == "Untitled Entry"
