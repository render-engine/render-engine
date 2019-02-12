from jinja2 import Markup
from string import punctuation
from markdown import markdown
from pages.page import Page


class BlogPost(Page):
    def __init__(self, base_file, output_path, template='blog.html'):
        super().__init__(base_file=base_file, output_path=output_path, template=template)
        self.tags = self.get_tags()
        self.summary = Markup(markdown(getattr(self, '_summary',
                self.summary_from_content(self.content)) + '...'))

    def get_tags(self):
        tags = getattr(self, '_tags', '')
        return tags.split(',')

    def summary_from_content(self, content):
        print(len(content))
        start_index = min(140, len(content) - 1)
        print(start_index) 
        while content[start_index] not in punctuation:
            start_index -= 1
        
            if not start_index:
                  return content
              
        return self.content[:start_index]
