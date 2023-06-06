sphinxcontrib-docstring-parser
==============================

|badge:pypi-version| |badge:py-versions|
|badge:pre-commit| |badge:pre-commit.ci|
|badge:black| |badge:prettier|

.. |badge:pypi-version| image:: https://img.shields.io/pypi/v/sphinxcontrib-docstring-parser.svg
   :target: https://pypi.org/project/sphinxcontrib-docstring-parser
   :alt: [Latest PyPI version]
.. |badge:py-versions| image:: https://img.shields.io/pypi/pyversions/sphinxcontrib-docstring-parser.svg
   :target: https://pypi.org/project/sphinxcontrib-docstring-parser
   :alt: [Supported Python versions]
.. |badge:pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen.svg?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: [pre-commit: enabled]
.. |badge:pre-commit.ci| image:: https://results.pre-commit.ci/badge/github/sphinx-contrib/doctring_parser/main.svg
   :target: https://results.pre-commit.ci/latest/github/sphinx-contrib/doctring_parser/main
   :alt: [pre-commit.ci status]
.. |badge:black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: [Code style: black]
.. |badge:prettier| image:: https://img.shields.io/badge/code_style-prettier-ff69b4.svg
   :target: https://github.com/prettier/prettier
   :alt: [Code style: prettier]


This package provides ``sphinxcontrib.doctring_parser``, a code parser to get shinx-needs objects for
Sphinx-based documentation.


Installation
------------

1. ``pip install sphinxcontrib-docstring-parser``


Configuration
-------------

1. Add ``'sphinxcontrib.doctring_parser'`` to the ``extensions`` list in ``conf.py``.

   .. code::

      extensions = [ 'sphinxcontrib.doctring_parser' ]


Usage
-----

Manual Mode
^^^^^^^^^^^

To parser a file or folder use ``doc_parser`` role:

.. code::

   .. doc_parser: Title
      :folders: ["src","test"]

Renders as "Name Surname" with the appropriate mailto link.

.. code::

   :email:`user@myplace.org`

Renders as "user@myplace.org" with the appropriate mailto link
