from .archive import Archive


class Blog:
    archive = Archive()
    archive_sort = "_date_published"
    reverse = True

    @property
    def pages(self):
        return self.archive.pages

    @property
    def _date_published(self):
        publish_options = [
            "date_published",
            "date",
            "publish_date",
            "date_modified",
            "modified_date",
        ]

        for option in publish_options:
            if hasattr(self, option):
                return getattr(self, option)

    def __getattr__(self, name):
        return getattr(self.archive, name)
