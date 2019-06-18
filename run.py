import json
import config
import shutil
from pathlib import Path
from paginate import write_paginated_pages
from page import Page
from blog import BlogPost
from engine import Engine
from links import Link
from feeds import feed_gen
from collection import Collection


engine = Engine()

pages = Collection(
        name='pages',
        content_type=Page,
        content_path='pages',
        )

blog = Collection(name='blog',
        content_type=BlogPost,
        output_path='blog',
        )

services = Collection(
        name='services',
        content_type=Page,
        output_path='services',
        content_path='services',
        )

engine.collections = (pages, blog, services)

@engine.build(Page, template='index.html', route='/index')
def index():
    services = [
            Link(
                name='Editing',
                url='editing.html',
                image='fa-laptop-code',
                ),
            Link(
                name="Coaching",
                url="coaching.html",
                image='fa-hands-helping',
                ),
            ]
    return (services)

@engine.build(
        Page,
        template='coaching/coaching_feedback.html',
        route='/coaching_feedback',
        )
def coaching_feedback():
    return ()

@engine.build(
        Page,
        template='coaching/coaching_feedback.html',
        route='/dev-podcaster-course',
        )
def podcasting_course():
    return Page(template='courses.html').html

def pagination():
    write_paginated_pages(blog.name, blog.paginate, path=blog.output_path, template='blog_list.html')

def categorization():
    category_filename = f'{blog.output_path}/categories'
    category_path = Path(category_filename)
    category_path.mkdir(parents=True, exist_ok=True)
    write_page(f'{category_path}/all.html',
            Page(template='categories.html',
            topic_list=[c for c in blog.categories]).html)

    for category in blog.categories:
        write_page(f'{category_path}/{category}.html',
                Page(template='blog_list.html',
                    post_list=blog.categories[category],
                    output_path=blog.output_path).html)
        feed_gen(
                blog,
                page_filter=blog.categories[category],
                output_path=category_path,
                name=category,
                )

    tag_path = Path(f'{blog.output_path}/tag')
    tag_path.mkdir(parents=True, exist_ok=True)
    write_page(f'{tag_path}/all.html', Page(template='categories.html',
        topic_list=[t for t in blog.tags]).html)

    for tag in blog.tags:
        write_page(f'{tag_path}/{tag}.html',
                Page(template='blog_list.html',
                post_list=blog.tags[tag],
                output_path=blog.output_path).html)




if __name__ == "__main__":
    # This will all become render_engine.run()
    # Overwrite Existing Tree then generate a new tree.
    engine.run()
