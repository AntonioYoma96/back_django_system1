import os
import sys

cwd = os.getcwd()
parent = os.path.dirname(cwd)
sys.path.append(parent)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


# -- Project information -----------------------------------------------------

project = 'SmartPeople 2.0'
copyright = '2020, Felipe Maldonado'
author = 'Felipe Maldonado'

# The full version, including alpha/beta/rc tags
release = '0.1.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']

language = 'es'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'

html_static_path = ['_static']
