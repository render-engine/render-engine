from .collection import Collection
from .page import Page


class Archive(Collection):
    archive_template = "archive.html"
    archive_slug = "all_posts"
    archive_content_type = Page
    reverse = False

    @property
    def pages(self):
        pages = super().pages
        pages.append(self._create_archive_page(pages))
        return pages

    def _generate_archive_page_pages(self, collection_pages):
        page_dot_pages = sorted(
            collection_pages, key=lambda page: page._slug, reverse=self.reverse
        )
        return page_dot_pages

    def _create_archive_page(self, archive_pages):
        page = self.archive_content_type()
        page.template = self.archive_template
        page.slug = self.archive_slug
        pages = self._generate_archive_page_pages(archive_pages)
        page.pages = pages
        return page
