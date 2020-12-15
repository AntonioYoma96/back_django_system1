import os
import sys
import django
sys.path.insert(0, os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()


# Project information

project = 'SmartPeople 2'
copyright = '2020, Felipe Maldonado'
author = 'Felipe Maldonado'

release = '0.1.1'

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']

language = 'es'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML options
html_theme = 'alabaster'

html_static_path = ['_static']

html_theme_options = {
    "fixed_sidebar": True,
    "page_width": '1000px',
    "sidebar_width": '235px',
}
