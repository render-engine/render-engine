# Hookspecs

## Classes

### `PluginManager`

#### Functions

##### `REGISTER_PLUGIN(PLUGIN)`

Register a plugin with the site

### `SiteSpecs`

Plugin hook specifications for the Site class

#### Functions

##### `ADD_DEFAULT_SETTINGS(SITE)`

Add default settings to the site

##### `POST_BUILD_COLLECTION(SITE, SETTINGS)`

Build After Building the collection

##### `POST_BUILD_SITE(SITE)`

Build After Building the site

##### `POST_RENDER_CONTENT(PAGE, SETTINGS, SITE)`

Augments the content of the page before it is rendered as output.

##### `PRE_BUILD_COLLECTION(COLLECTION, SETTINGS)`

Steps Prior to Building the collection

##### `PRE_BUILD_SITE(SITE, SETTINGS)`

Steps Prior to Building the site

##### `RENDER_CONTENT(PAGE, SETTINGS)`

Augments the content of the page before it is rendered as output.
