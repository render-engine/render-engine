"""
Core rendering engine module for Render Engine.

This module sets up the Jinja2 templating environment used throughout the site generation process.
It configures template loaders to support user templates, theme templates, and built-in templates,
and provides custom filters for common rendering tasks like date formatting and URL generation.
"""

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

# Template loader hierarchy for the rendering engine
# This ChoiceLoader tries loaders in order, allowing user templates to override built-in ones
render_engine_templates_loader = ChoiceLoader(
    [
        # User-defined template directories
        FileSystemLoader("templates"),
        # Theme-specific templates loaded via prefix (e.g., 'theme_name/template.html')
        PrefixLoader(
            {
                # "prefix": theme.loader - populated dynamically when themes are registered
            }
        ),
        # Built-in templates from the render_engine package (lowest priority fallback)
        PackageLoader("render_engine", "render_engine_templates"),
    ]
)

# Main Jinja2 environment for template rendering
# Configured with autoescaping for XML/HTML safety and whitespace trimming for cleaner output
engine = Environment(
    loader=render_engine_templates_loader,
    autoescape=select_autoescape(["xml"]),  # Auto-escape XML and HTML files
    lstrip_blocks=True,  # Strip leading whitespace from template blocks
    trim_blocks=True,  # Trim trailing newlines from template blocks
)


# Custom Jinja2 filters for template rendering


def to_pub_date(value: datetime.datetime | datetime.date) -> str:
    """
    Convert a datetime/date object to RFC 2822 formatted string for RSS/Atom feeds.

    This filter handles both datetime and date objects, converting dates to datetimes
    and formatting them according to email/RSS standards.

    Args:
        value: The datetime or date object to format

    Returns:
        str: RFC 2822 formatted datetime string
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
    """
    Format a datetime/date object using a specified format string.

    Uses the site's DATETIME_FORMAT from globals if no format is provided.

    Args:
        env: Jinja2 environment (passed automatically)
        value: The datetime/date object to format
        datetime_format: Optional format string (defaults to site setting)

    Returns:
        str: Formatted datetime string
    """
    if datetime_format:
        format = datetime_format
    else:
        format = env.globals.get("DATETIME_FORMAT", "%Y-%m-%d")

    return value.strftime(format)


engine.filters["format_datetime"] = format_datetime


@pass_environment
def to_absolute(env: Environment, url: str) -> str:
    """
    Convert a relative URL to an absolute URL using the site's base URL.

    Args:
        env: Jinja2 environment (passed automatically)
        url: Relative URL to convert

    Returns:
        str: Absolute URL
    """
    return str(urljoin(env.globals.get("SITE_URL"), url))


engine.filters["to_absolute"] = to_absolute


@pass_environment
def feed_url(env: Environment, value: str) -> str:
    """
    Generate the URL for a collection's RSS/Atom feed.

    Args:
        env: Jinja2 environment (passed automatically)
        value: Name/slug of the collection

    Returns:
        str: URL to the collection's feed

    Raises:
        ValueError: If the collection is not found in routes
    """
    routes = env.globals.get("routes")

    if routes:
        return routes[value].feed.url_for()
    else:
        raise ValueError("No Route Found")


engine.filters["feed_url"] = feed_url


@pass_environment
def url_for(env: Environment, value: str, page: int = 0) -> str:
    """
    Resolve route identifiers to URLs across the entire site.

    This filter provides cross-referencing between pages and collections,
    enabling templates to generate links to any content in the site.

    Route Resolution Patterns:

    1. Direct Page/Collection Reference:
       {{ "about" | url_for }} → URL for page/collection named "about"

    2. Collection Page Reference:
       {{ "blog.my-post" | url_for }} → URL for "my-post" in "blog" collection

    3. Collection Archive Reference:
       {{ "blog" | url_for(1) }} → URL for second archive page of "blog" collection

    Template Usage Examples:
        <a href="{{ 'blog' | url_for }}">Blog Index</a>
        <a href="{{ 'blog.hello-world' | url_for }}">Specific Post</a>
        <a href="{{ 'blog' | url_for(2) }}">Blog Page 2</a>

    Args:
        env: Jinja2 environment (passed automatically)
        value: Route identifier ("collection" or "collection.page")
        page: Archive page number for collections (default: 0)

    Returns:
        str: Relative URL for the resolved route

    Raises:
        ValueError: If route cannot be resolved
    """
    routes = env.globals.get("routes")
    route_parts = value.split(".", maxsplit=1)

    if len(route_parts) == 2:
        # Handle collection.page format - find specific page within collection
        collection_name, page_slug = route_parts
        if collection := routes.get(collection_name, None):
            for page_obj in collection:
                if getattr(page_obj, page_obj._reference) == page_slug:
                    return page_obj.url_for()
    else:
        # Handle direct collection/page reference
        route = routes.get(value)
        if isinstance(route, Collection):
            # Return URL for specified archive page (supports pagination)
            return list(route.archives)[page].url_for()
        return route.url_for()

    raise ValueError(f"{value} is not a valid route.")


engine.filters["url_for"] = url_for
