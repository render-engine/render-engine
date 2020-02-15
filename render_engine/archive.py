import logging

from .collection import Collection
from .page import Page


class Archive(Collection):

    @property
    def pages(self):
        pages = super().pages
        pages.append(self._create_archive_page(pages))
        return pages

    def _generate_archive_page_pages(self, collection_pages):
        return page_dot_pages

    def _create_archive_page(self, archive_pages):
        page = self.archive_content_type()
        page.template = self.archive_template
        page.slug = self.archive_slug
        pages = self._generate_archive_page_pages(archive_pages)
        page.pages = pages
        return page
