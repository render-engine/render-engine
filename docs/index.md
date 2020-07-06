Render Engine
-----

Render Engine is designed to think in terms of pages.

Render Engine's components build off of one another.

At the base level there is a **Page**, it is just that, a single entity of HTML and metadata goodness.

Sometimes a lot of pages will have a lot in common or belong to a group. We call these **Collections**. Collections can have any number of the same, or different attributes. Oh and your collections can even have collections...🤯

All of these pages we build need a home. This is a **Site**. A site serves as a container for your pages controlling it's structure and how pages are built.

Last but not least is the **Engine**. And engine is what is doing the work building out your pages from the data and templates that you have provided it. How do you start that engine? Simple.

**`site.render()`**
