import logging
import maya
from render_engine import Collection

class Blog(Collection):
    @property
    def is_valid(self):
        checks = {
                'title': getattr(self, 'title', False),
                'link': getattr(self, 'link', False),
                }
        return check_validity(checks)

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

def check_validity(checks):
    logging.debug(checks.items())
    if all(list(map(lambda x: x[1], checks.items()))):
        return True

    else:
        invalid = filter(lambda x: x[1] == False, checks.items())
        for item in invalid:
            print(f'{item[0]} does not have a valid value: {item[1]}')
        return False

