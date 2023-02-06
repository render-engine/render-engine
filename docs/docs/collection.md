::: render_engine.collection


***NOTE***
Subcollections Used to exist but have been removed. They should be added again soon as a built-in plugin.

## Attributes

    These are the attributes that the Collection will look for:

    - `content_path_filter`: Callable[[pathlib.Path], bool] | None
    archive_template: str | None
    content_path: pathlib.Path
    content_type: Type[Page] = Page
    Feed: Type[RSSFeed]
    feed_title: str
    include_extensions: list[str] = ["*.md", "*.html"]
    items_per_page: int | None
    PageParser: Type[BasePageParser] = MarkdownPageParser
    parser_extras: dict[str, Any]
    routes: list[_route] = ["./"]
    sort_by: str = "title"
    sort_reverse: bool = False
    title: str
    template: str | None
