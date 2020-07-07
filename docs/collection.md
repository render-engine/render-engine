Collection
----

A Collection is great when you have many pages with similar attributes or pages
that should be grouped together.

Collection attributes will be applied to each page in the collection.

Not So Safe Attributes
====

### engine

`engine: Optional[str]=None # _inherits from Site_`

The engine needs to be added to the site dictionary of engines.

```
import Mako

class mako(Engine):
  ... # code for mako to be compatible with Render Engine

site = Site()
site.engines['Mako'] = mako

class MyCollection():
  engine = 'Mako'
```

The page's Engine of the is responsible for generating content for your
webpage. In most cases this will be provided by the site and should not be
changed.

