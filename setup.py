"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from os import path

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
# from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='render_engine',  # Required
    version='2021.9.0',  # Required
    description='Static Page Generation with Flask-like simplicity and flair ✨',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://render-engine.site',  # Optional
    author='Jay Miller',  # Optional
    author_email='jay@productivityintech.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Text Processing :: Markup :: HTML',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Natural Language
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='static site web framework',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    python_requires='>=3.8',
    install_requires=[
    'pendulum',
    'pygments',
    'markdown2',
    'progress',
    'jinja2',
    'more-itertools',
    'click',
    'python-slugify',
    'python-frontmatter',
    ],  # Optional
    extras_require={  # Optional
        'dev': ['check-manifest', 'elasticsearch', 'elastic_app_search'],
        'test': ['pytest', 'pytest-cov', 'black'],
    },

    package_data={  # Optional
    #    'sample': ['package_data.dat'],
         'render_engine': ['rss/*', 'templates/*', 'run_template.txt'],
    },
    entry_points={  # Optional
        'console_scripts': [
            'render-engine=render_engine.__main__:main',
            'render-engine-quickstart=render_engine.quickstart:quickstart',
        ],
    },
    project_urls={  # Optional
        'Documentation': 'https://render-engine.readthedocs.io/en/latest',
        'Bug Reports': 'https://github.com/kjaymiller/render_engine/issues',
        'Funding': 'https://paypal.me/kjaymiller',
        'Say Thanks!': 'http://saythanks.io/to/kjaymiller',
        'Source': 'https://github.com/kjaymiller/render_engine/',
    },
)
