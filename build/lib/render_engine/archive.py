import logging

from .collection import Collection
from .page import Page


class Archive:
    collection = Collection()
    content_type = Page
    archive_template = "archive.html"
    archive_slug = "all_posts"
    archive_sort = "_slug"
    reverse = False

    @property
    def pages(self):
        class_name = self.__class__.__name__
        pages = self.collection.pages
        archive_pages = self.generate_archive()
        pages.append(archive_pages)
        return pages

    def generate_archive(self):
        logging.debug(f"generating archive")
        page = self.content_type()
        logging.debug(f"page - {page}")

        pages = sorted(
            self.collection.pages,
            key=lambda x: getattr(x, self.archive_sort),
            reverse=self.reverse,
        )

        logging.debug(f"pages - {pages}")
        page.pages = pages
        page.template = self.archive_template
        page.slug = self.archive_slug
        return page

    def __getattr__(self, name):
        return getattr(self.collection, name)
