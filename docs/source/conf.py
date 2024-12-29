import pathlib
import sys

src_dir = pathlib.Path(__file__).parents[2].resolve() / "src"
sys.path.insert(0, src_dir.as_posix())
print(f"sys.path is {sys.path}")

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "sd44的Python小脚本"
copyright = "2024, sd44 sd44sd44@yeah.net"
author = "sd44"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "autodoc2",
    "sphinx.ext.napoleon",
]

autodoc2_packages = [
    "../../src/showcode",
]
templates_path = ["_templates"]
exclude_patterns = []

language = "zh_CN"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
