Contributing
------------

Requirements
============

When submitting a pull request, please ensure your changes meet the following
requirements:

* Pull request points to dev_ (development) branch.
* Changes are squashed into a single commit.
* Commit message is in present tense (e.g. "Add foo" over "Added foo").
* Sphinx_-compatible docstrings.
* PEP8_ compliance.
* Test coverage_ remains at %100.
* No build failures on TravisCI_.
* Up-to-date documentation (see below).
* Maintains backward-compatibility.
* Maintains compatibility with Python 2.7+ and 3.4+.

Style
=====

Run flake8_ to check style:

.. code-block:: bash

    ~$ pip install flake8
    ~$ git clone https://github.com/joowani/binarytree.git
    ~$ cd binarytree
    ~$ flake8


Testing
=======

Run unit tests:

.. code-block:: bash

    ~$ pip install pytest
    ~$ git clone https://github.com/joowani/binarytree.git
    ~$ cd binarytree
    ~$ py.test --verbose

Run unit tests with coverage:

.. code-block:: bash

    ~$ pip install coverage pytest pytest-cov
    ~$ git clone https://github.com/joowani/binarytree.git
    ~$ cd binarytree
    ~$ py.test --cov=binarytree --cov-report=html

    # Open the generated file htmlcov/index.html in a browser

Documentation
=============

Documentation uses reStructuredText_ and Sphinx_. To build locally:

.. code-block:: bash

    ~$ pip install sphinx sphinx_rtd_theme
    ~$ git clone https://github.com/joowani/binarytree.git
    ~$ cd binarytree/docs
    ~$ sphinx-build . build
    # Open build/index.html in a browser


.. _dev: https://github.com/joowani/binarytree/tree/dev
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _coverage: https://coveralls.io/github/joowani/binarytree
.. _TravisCI: https://travis-ci.org/joowani/binarytree
.. _Sphinx: https://github.com/sphinx-doc/sphinx
.. _flake8: http://flake8.pycqa.org
.. _reStructuredText: https://en.wikipedia.org/wiki/ReStructuredText
