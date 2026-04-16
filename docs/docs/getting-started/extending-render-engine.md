---
title: "Extending Render Engine"
description: "Extending Render Engine with custom plugins and themes."
date: April 16, 2026
tags: ["customization", "themes", "plugins", "render-engine"]
---
While Render Engine works great out of the box, there are times when you might
want to extend it beyond the basics. To do this, you can use themes, plugins,
and content managers.

## Themes

Themes s are a collection of Jinja templates and static files used to render
your site.

For more information on themes, check out the [ThemeManager page].

## Plugins

Plugins are units of code that run at different points during the rendering
process. Plugins can do things like transformations, rendering different
types of content, adjusting formatting beyond what the parser handles, and
more.

For more information on writing and using plugins, check out the
[Plugins page].

## Content Managers

Render Engine uses Content Managers to handle loading the content. Render
Engine comes with a file system based content manager, but you could write
your own to pull your content from a database, JSON file, or something else.

For more information on writing and using plugins, check out the
[Content Managers page].

> **Note:** To find some of our favorite themes and plugins checkout out
> [The Render Engine Awesome List]

## Continue to [Building your Site]

[ThemeManager Page]:../theme_management/
[Plugins Page]:../plugins/
[Content Managers Page]:../content_manager/
[The Render Engine Awesome List]:https://github.com/render-engine/render-engine-awesome-list
[building your site]: building-your-site.md
