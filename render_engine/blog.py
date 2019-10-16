import logging

import maya
from more_itertools import unique_everseen

from .collection import Collection


class Blog(Collection):
    default_sort_field = 'date_published'
    reverse_sort = True
    tag_separator = ','

    _categories = _tags = set()

    @property
    def categories(self):
        for page in self.pages:
            if getattr(page, 'category', None):
                self._categories.add(page.category)
        return [filter_pages('category', category) for category in _categories]

    @property
    def tags(self):
        for page in self.pages:
            if getattr(page, 'tags', None):
                _tags.add(page.tags.split(self.tag_separator))

        return [filter_pages('tags', tag, multiple=True) for tag in _tags]

    @property
    def is_valid(self):
        checks = {
                'title': getattr(self, 'title', False),
                'link': getattr(self, 'link', False),
                }
        return check_validity(checks)

    @staticmethod
    def check_validity(checks):
        logging.debug(checks.items())
        if all(list(map(lambda x: x[1], checks.items()))):
            return True

        else:
            invalid = filter(lambda x: x[1] == False, checks.items())
            for item in invalid:
                print(f'{item[0]} does not have a valid value: {item[1]}')
            return False

    @property
    def show_warnings(self):
        self.is_valid()

        for page in self.pages:
            has_created_time = getattr(page, 'created_time', False)

            if has_created_time:
                created_time = maya.parse(has_created_time)

            else:
                created_time = False

            checks = {
                    'title': getattr(page, 'title', False),
                    'created_time': created_time,
                    }

        return check_validity(checks)

    @property
    def _iterators(self):
        return [self.pages, self.categories, self.tags]
