import datetime
import logging
import typing

import dateutil.parser
import more_itertools

from .collection import Collection
from .feeds import RSSFeed
from .page import Page
from .parsers.markdown import MarkdownPageParser


def _check_date_values(date_value_name:str, potential_attrs: typing.Iterable[str]) -> datetime.date | datetime.datetime:
    """
    Checks potential attrs for a date value.
    This will raise an error if the value is not a datetime object.
    """
    
    set_attr = more_itertools.first_true(potential_attrs)

    if set_attr is None:
        raise ValueError(
            f"""Error Parsing {date_value_name}. No date value found."""
        )

    if isinstance(set_attr, datetime.datetime) or isinstance(set_attr, datetime.date):
        return set_attr.replace(tzinfo=None)
        
    else:
        logging.warning(
                f"""
                date_modified={set_attr} equated as string and not datetime.
                Render Engine will attempt to parse as a datetime object. For Best Results use RFC2822 format.
                
                For more information, see: https://render-engine.readthedocs.io/en/latest/blog.html#date-published-and-date-modified
                """
        )
        return dateutil.parser.parse(set_attr).replace(tzinfo=None)


class BlogPost(Page):
    """Page Like object with slight modifications to work with BlogPosts."""

    list_attrs = ["tags"]
    invalid_attrs = ["slug", "date_published", "date_modified"]

    @property
    def date_modified(self):
        valid_date_modified_values = (
                getattr(self, "_date_modified", None),
                getattr(self, "modified_date", None),
                getattr(self, "date", None),
            )
        return _check_date_values("date_modified", valid_date_modified_values)

    @property
    def date_published(self):
        valid_date_published_values = (
                getattr(self, "_date_published", None),
                getattr(self, "publish_date", None),
                getattr(self, "date", None),
            )
    
        return _check_date_values("date_published", valid_date_published_values)

class Blog(Collection):
    """
    Custom :py:class:`collection.Collection` class with archiving enabled, sort by `date_published` by default.

    Todos:
        - Add Support for JSON Feeds
        - Rename the archive items so they are not private
    """

    BasePageParser = MarkdownPageParser
    content_type: typing.Type[BlogPost] = BlogPost
    sort_reverse: bool = True
    sort_by = "date_published"
    has_archive = True
    Feed = RSSFeed
