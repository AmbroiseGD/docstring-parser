
from sphinx.util import logging
from importlib import metadata
from .py_docstring_parser import *

__version__ = metadata.version("sphinxcontrib_docstring_parser")
logger = logging.getLogger("sphinxcontrib_docstring_parser")


def setup(app):
    app.add_directive("doc_parser", docstrings_parser)

    return {
        "version": ".".join(__version__.split(".")[:3]),
        "parallel_read_safe": False,
        "parallel_write_safe": False,
    }