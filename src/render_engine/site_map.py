from collections.abc import Generator, Iterable
from pathlib import Path
from urllib.parse import urljoin

import slugify

from render_engine import Collection, Page
from render_engine._base_object import BaseObject


class SiteMapEntry:
    """Entry in the site map"""

    def __init__(self, entry: BaseObject, route: str | Path, from_collection=False):
        """Initialize the entry"""
        self.slug = entry._slug
        self.title = entry.title
        self.path_name = entry.path_name
        match entry:
            case Page():
                self._route = Path("/") / (route / self.path_name if from_collection else self.path_name)
                self.entries = list()
            case Collection():
                self._route = Path("/") / route
                self.entries = [
                    SiteMapEntry(collection_entry, self._route, from_collection=True) for collection_entry in entry
                ]
            case _:
                pass

    @property
    def url_for(self) -> str:
        """The URL for the given entry"""
        return str(self._route)

    @property
    def all_urls(self) -> Generator[str]:
        yield from map(str, (entry.url_for for entry in self.entries))


class SiteMap:
    """Site map"""

    def __init__(self, route_list: dict, site_url: str):
        self._route_map = dict()
        self._collections = dict()
        for route, entry in route_list.items():
            sm_entry = SiteMapEntry(entry, route)
            self._route_map[sm_entry.slug] = sm_entry
            if sm_entry.entries:
                self._collections[sm_entry.slug] = sm_entry
        self.site_url = site_url

    def find(
        self,
        attr: str,
        value: str,
        collection: str = None,
        full_search: bool = False,
    ) -> SiteMapEntry | None:
        """
        Find an entry in the site map

        Only one of the parameters slug, path_name, or title may be set.
        If collection is set that collection will be searched. If it is not set then all collections
        will be searched if full_search is True.
        If there would be a match in multiple collections - or for just a page, the first match will be returned.

        :param slug: Slug of the entry to find
        :param path_name: Path name of the entry
        :param title: The title to look for
        :param collection: The name of the collection to search
        :param full_search: Search recursively in collections
        :return: The first found match or None if not found
        """

        def _search(attr: str, value: str, entries: Iterable) -> SiteMapEntry | None:
            """
            Search the list of entries for a match

            :param attr: The attribute to search by
            :param value: The value to search for
            :param entries: List of entries to search
            :return: First found match or None if not found
            """
            for entry in entries:
                if getattr(entry, attr, None) == value:
                    return entry
            return None

        if collection:
            # Collection was specified so check there first
            collection = slugify.slugify(collection)
            if not (_collection := self._collections[collection]):
                return None
            if value and (entry := _search(attr, value, _collection.entries)):
                return entry
            return None
        if attr == "slug" and (entry := self._route_map.get(value)):
            # Looking for a slug
            return entry
        # Check the base
        if value and (entry := _search(attr, value, self._route_map.values())):
            return entry
        if full_search:
            # Check each collection
            for _collection in self._collections.values():
                if entry := _search(attr, value, _collection.entries):
                    return entry
        return None

    @property
    def html(self) -> str:
        """Build the site map as HTML"""
        html_string = "<ul>\n"
        for entry in self._route_map.values():
            html_string += f'\t<li><a href="{urljoin(self.site_url, entry.url_for)}">{entry.title}</a></li>\n'
            if entry.entries:
                html_string += "\t<ul>\n"
                html_string += "".join(
                    f'\t\t<li><a href="{urljoin(self.site_url, sub_entry.url_for)}">{sub_entry.title}</a></li>\n'
                    for sub_entry in entry.entries
                )
                html_string += "\t</ul>\n"
        html_string += "</ul>\n"
        return html_string
