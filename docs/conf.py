# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# https://sphinx-copybutton.readthedocs.io/en/latest/index.html
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'ronataswestoldturkic'
copyright = '2023, Viktor Martinović'
author = 'Viktor Martinović'
version = '2.0'
release = '2.0'
extensions = ['sphinx.ext.autodoc', 'sphinx_copybutton']
html_theme = 'sphinx_rtd_theme'

# uncomment row below if  installation problems with dependencies
autodoc_mock_imports = [
    "epitran>=1.24",
    "ipatok>=0.4.1",
    "lingpy>=2.6.9",
    "loanpy>=3.0.0",
    "matplotlib<=3.5.3"
]
