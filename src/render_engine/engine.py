import datetime
from email.utils import format_datetime as fmt_datetime
from urllib.parse import urljoin

from dateutil.parser import parse
from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    PrefixLoader,
    pass_environment,
    select_autoescape,
)

from .collection import Collection

render_engine_templates_loader = ChoiceLoader(
    [
        # Newly Registered Themes 'templates folder' goes here
        FileSystemLoader("templates"),
        PrefixLoader(
            {
                # "prefix": theme.loader
            }
        ),
        PackageLoader("render_engine", "render_engine_templates"),
    ]
)

engine = Environment(
    loader=render_engine_templates_loader,
    autoescape=select_autoescape(["xml"]),
    lstrip_blocks=True,
    trim_blocks=True,
)


def to_pub_date(value: datetime.datetime | datetime.date) -> str:
    """
    Parse information from the given class object.
    """

    if isinstance(value, datetime.date):
        value = parse(value.isoformat())
    return fmt_datetime(value)


engine.filters["to_pub_date"] = to_pub_date


@pass_environment
def format_datetime(
    env: Environment,
    value: datetime.datetime | datetime.date,
    datetime_format: str | None = None,
) -> str:
    """Parse information from the given class object."""
    if datetime_format:
        format = datetime_format
    else:
        format = env.globals.get("DATETIME_FORMAT", "%Y-%m-%d")

    return value.strftime(format)


engine.filters["format_datetime"] = format_datetime


@pass_environment
def to_absolute(env: Environment, url: str) -> str:
    return str(urljoin(env.globals.get("SITE_URL"), url))


engine.filters["to_absolute"] = to_absolute


@pass_environment
def feed_url(env: Environment, value: str) -> str:
    """Returns the URL for the collections feed"""
    routes = env.globals.get("routes")

    if routes:
        return routes[value].feed.url_for()

    else:
        raise ValueError("No Route Found")


engine.filters["feed_url"] = feed_url


@pass_environment
def url_for(env: Environment, value: str, page: int = 0) -> str:
    """Look for the route in the route_list and return the url for the page."""
    routes = env.globals.get("routes")
    route = value.split(".", maxsplit=1)

    if len(route) == 2 and isinstance(route, list):
        collection, route = route
        if collection := routes.get(collection, None):
            for page in collection:
                if getattr(page, page._reference) == route:
                    return page.url_for()

    else:
        route = routes.get(value)
        if isinstance(route, Collection):
            return list(route.archives)[page].url_for()
        return route.url_for()

    raise ValueError(f"{value} is not a valid route.")


engine.filters["url_for"] = url_for
