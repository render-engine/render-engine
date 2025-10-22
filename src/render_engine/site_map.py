from collections.abc import Iterable
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
        self.title = entry._title
        self.path_name = entry.path_name
        match entry:
            case Page():
                # For a base page the _route created if we use the route is invalid - just use the path_name
                self._route = f"/{route.lstrip('/')}/{self.path_name}" if from_collection else f"/{self.path_name}"
                self.entries = list()
            case Collection():
                self._route = f"/{entry.routes[0].lstrip('/')}"
                self.entries = [
                    SiteMapEntry(collection_entry, self._route, from_collection=True) for collection_entry in entry
                ]
            case _:
                pass

    @property
    def url_for(self) -> str:
        """The URL for the given entry"""
        return str(self._route)

    def __str__(self) -> str:
        """String representation of the entry as its URL"""
        return self.url_for


class SiteMap:
    """Site map"""

    def __init__(self, route_list: dict, site_url: str):
        """
        Create the site map based on the route_list

        :param route_list: The route list to parse
        :param site_url: Used for rendering the HTML to have absolute URLs.
        """
        self._route_map = dict()
        self._collections = dict()
        route: str
        entry: BaseObject
        for route, entry in route_list.items():
            if entry.skip_site_map:
                continue
            sm_entry = SiteMapEntry(entry, route)
            self._route_map[sm_entry.slug] = sm_entry
            if sm_entry.entries:
                self._collections[sm_entry.slug] = sm_entry
        self.site_url = site_url

    def __iter__(self):
        """Iterator for the site map object"""
        for entry in self._route_map.values():
            yield entry
            yield from entry.entries

    def find(
        self,
        value: str,
        attr: str = "slug",
        collection: str = None,
        full_search: bool = False,
    ) -> SiteMapEntry | None:
        """
        Find an entry in the site map

        Only one of the parameters slug, path_name, or title may be set.
        If collection is set that collection will be searched. If it is not set then all collections
        will be searched if full_search is True.
        If there would be a match in multiple collections - or for just a page, the first match will be returned.

        :param value: The value of attribute to search for
        :param attr: The name of attribute to search for, defaults to slug
        :param collection: The name of the collection to search
        :param full_search: Search recursively in collections
        :return: The first found match or None if not found
        """

        def search(s_attr: str, s_value: str, entries: Iterable) -> SiteMapEntry | None:
            """
            Search the list of entries for a match

            :param s_attr: The attribute to search by
            :param s_value: The value to search for
            :param entries: List of entries to search
            :return: First found match or None if not found
            """
            for s_entry in entries:
                if getattr(s_entry, s_attr, None) == s_value:
                    return s_entry
            return None

        if not value:
            return None
        if collection:
            # Collection was specified so check there
            return (
                search(attr, value, _collection.entries)
                if (_collection := self._collections[slugify.slugify(collection)])
                else None
            )
        if attr == "slug":
            # We can handle slug a bit differently since it's the key to the route map dictionary.
            if entry := self._route_map.get(value):
                return entry
        # Check the base route map
        elif entry := search(attr, value, self._route_map.values()):
            return entry
        if full_search:
            # Check each collection
            for collection in self._collections.values():
                if entry := search(attr, value, collection.entries):
                    return entry
        return None

    @property
    def html(self) -> str:
        """Build the site map as HTML"""
        html_string = "<ul>\n"
        # We can't iterate over `self` because that will flatten out the site map and we do not want that for the HTML
        # version.
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
