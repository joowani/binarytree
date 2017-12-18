Binarytree: Python Library for Learning Binary Trees
----------------------------------------------------

.. image:: https://travis-ci.org/joowani/binarytree.svg?branch=master
    :target: https://travis-ci.org/joowani/binarytree
    :alt: Build Status

.. image:: https://badge.fury.io/py/binarytree.svg
    :target: https://badge.fury.io/py/binarytree
    :alt: Package Version

.. image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg
    :target: https://github.com/joowani/binarytree
    :alt: Python Versions

.. image:: https://coveralls.io/repos/github/joowani/binarytree/badge.svg?branch=master
    :target: https://coveralls.io/github/joowani/binarytree?branch=master
    :alt: Test Coverage

.. image:: https://img.shields.io/github/issues/joowani/binarytree.svg
    :target: https://github.com/joowani/binarytree/issues
    :alt: Issues Open

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/joowani/binarytree/master/LICENSE
    :alt: MIT License

|

.. image:: https://user-images.githubusercontent.com/2701938/34109703-4a8810aa-e3b9-11e7-8138-68eec47cfddb.gif
    :alt: Demo GIF

Introduction
============

Are you studying binary trees for your next exam, assignment or technical interview?

**Binarytree** is a Python library which provides a simple API to generate,
visualize, inspect and manipulate binary trees. It allows you to skip the
tedious work of setting up test data, and dive straight into practising
your algorithms! Heaps and BSTs (binary search trees) are also supported.

Announcements
=============

* **Binarytree** has been completely overhauled in version `3.0`_!
* Please see the releases_ page for details on the latest updates.

.. _3.0: https://github.com/joowani/binarytree/releases/tag/3.0.0
.. _releases: https://github.com/joowani/binarytree/releases

Requirements
============

- Python 2.7, 3.4, 3.5 or 3.6
- Pip_ installer

.. _Pip: https://pip.pypa.io

Installation
============

To install a stable version from PyPi_:

.. code-block:: bash

    ~$ pip install binarytree


To install the latest version directly from GitHub_:

.. code-block:: bash

    ~$ pip install -e git+git@github.com:joowani/binarytree.git@master#egg=binarytree

You may need to use ``sudo`` depending on your environment setup.

.. _PyPi: https://pypi.python.org/pypi/binarytree
.. _GitHub: https://github.com/joowani/binarytree


Getting Started
===============

By default, **binarytree** uses the following class to represent a node:

.. code-block:: python

    class Node(object):

        def __init__(self, value, left=None, right=None):
            self.value = value  # The node value
            self.left = left    # Left child
            self.right = right  # Right child


Generate and pretty-print various types of binary trees:

.. code-block:: python

    >>> from binarytree import tree, bst, heap
    >>>
    >>> # Generate a random binary tree and return its root node
    >>> my_tree = tree(height=3, is_perfect=False)
    >>>
    >>> # Generate a random BST and return its root node
    >>> my_bst = bst(height=3, is_perfect=True)
    >>>
    >>> # Generate a random max heap and return its root node
    >>> my_heap = heap(height=3, is_max=True, is_perfect=False)
    >>>
    >>> # Pretty-print the trees in stdout
    >>> print(my_tree)
    #
    #        _______1_____
    #       /             \
    #      4__          ___3
    #     /   \        /    \
    #    0     9      13     14
    #         / \       \
    #        7   10      2
    #
    >>> print(my_bst)
    #
    #            ______7_______
    #           /              \
    #        __3__           ___11___
    #       /     \         /        \
    #      1       5       9         _13
    #     / \     / \     / \       /   \
    #    0   2   4   6   8   10    12    14
    #
    >>> print(my_heap)
    #
    #              _____14__
    #             /         \
    #        ____13__        9
    #       /        \      / \
    #      12         7    3   8
    #     /  \       /
    #    0    10    6
    #

Use the `binarytree.Node`_ class to build your own trees:

.. _binarytree.Node:
    http://binarytree.readthedocs.io/en/latest/api.html#class-binarytree-node

.. code-block:: python

    >>> from binarytree import Node
    >>>
    >>> root = Node(1)
    >>> root.left = Node(2)
    >>> root.right = Node(3)
    >>> root.left.right = Node(4)
    >>>
    >>> print(root)
    #
    #      __1
    #     /   \
    #    2     3
    #     \
    #      4
    #


Inspect tree properties:

.. code-block:: python

    >>> from binarytree import Node
    >>>
    >>> root = Node(1)
    >>> root.left = Node(2)
    >>> root.right = Node(3)
    >>> root.left.left = Node(4)
    >>> root.left.right = Node(5)
    >>>
    >>> print(root)
    #
    #        __1
    #       /   \
    #      2     3
    #     / \
    #    4   5
    #
    >>> root.height
    2
    >>> root.is_balanced
    True
    >>> root.is_bst
    False
    >>> root.is_complete
    True
    >>> root.is_max_heap
    False
    >>> root.is_min_heap
    True
    >>> root.is_perfect
    False
    >>> root.is_strict
    True
    >>> root.leaf_count
    3
    >>> root.max_leaf_depth
    2
    >>> root.max_node_value
    5
    >>> root.min_leaf_depth
    1
    >>> root.min_node_value
    1
    >>> root.size
    5

    >>> root.properties  # To see all at once:
    {'height': 2,
     'is_balanced': True,
     'is_bst': False,
     'is_complete': True,
     'is_max_heap': False,
     'is_min_heap': True,
     'is_perfect': False,
     'is_strict': True,
     'leaf_count': 3,
     'max_leaf_depth': 2,
     'max_node_value': 5,
     'min_leaf_depth': 1,
     'min_node_value': 1,
     'size': 5}

    >>> root.leaves
    [Node(3), Node(4), Node(5)]

    >>> root.levels
    [[Node(1)], [Node(2), Node(3)], [Node(4), Node(5)]]

Use `level-order (breath-first)`_ indexes to manipulate nodes:

.. _level-order (breath-first):
    https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search

.. code-block:: python

    >>> from binarytree import Node
    >>>
    >>> root = Node(1)                  # index: 0, value: 1
    >>> root.left = Node(2)             # index: 1, value: 2
    >>> root.right = Node(3)            # index: 2, value: 3
    >>> root.left.right = Node(4)       # index: 4, value: 4
    >>> root.left.right.left = Node(5)  # index: 9, value: 5
    >>>
    >>> print(root)
    #
    #      ____1
    #     /     \
    #    2__     3
    #       \
    #        4
    #       /
    #      5
    #
    >>> # Use binarytree.Node.pprint instead of print to display indexes
    >>> root.pprint(index=True)
    #
    #       _________0-1_
    #      /             \
    #    1-2_____        2-3
    #            \
    #           _4-4
    #          /
    #        9-5
    #
    >>> # Return the node/subtree at index 9
    >>> root[9]
    Node(5)

    >>> # Replace the node/subtree at index 4
    >>> root[4] = Node(6, left=Node(7), right=Node(8))
    >>> root.pprint(index=True)
    #
    #       ______________0-1_
    #      /                  \
    #    1-2_____             2-3
    #            \
    #           _4-6_
    #          /     \
    #        9-7     10-8
    #
    >>> # Delete the node/subtree at index 1
    >>> del root[1]
    >>> root.pprint(index=True)
    #
    #    0-1_
    #        \
    #        2-3


Traverse the trees using different algorithms:

.. code-block:: python

    >>> from binarytree import Node
    >>>
    >>> root = Node(1)
    >>> root.left = Node(2)
    >>> root.right = Node(3)
    >>> root.left.left = Node(4)
    >>> root.left.right = Node(5)
    >>>
    >>> print(root)
    #
    #        __1
    #       /   \
    #      2     3
    #     / \
    #    4   5
    #
    >>> root.inorder
    [Node(4), Node(2), Node(5), Node(1), Node(3)]

    >>> root.preorder
    [Node(1), Node(2), Node(4), Node(5), Node(3)]

    >>> root.postorder
    [Node(4), Node(5), Node(2), Node(3), Node(1)]

    >>> root.levelorder
    [Node(1), Node(2), Node(3), Node(4), Node(5)]


`List representations`_ are also supported:

.. _List representations:
    https://en.wikipedia.org/wiki/Binary_tree#Arrays


.. code-block:: python

    >>> from binarytree import build
    >>>
    >>> # Build a tree from list representation
    >>> root = build([7, 3, 2, 6, 9, None, 1, 5, 8])
    >>> print(root)
    #
    #            __7
    #           /   \
    #        __3     2
    #       /   \     \
    #      6     9     1
    #     / \
    #    5   8
    #
    >>> # Convert the tree back to list representation
    >>> list(root)
    [7, 3, 2, 6, 9, None, 1, 5, 8]



Check out the documentation_ for more details!

.. _documentation: http://binarytree.readthedocs.io/en/latest/index.html


Contributing
============

Please have a look at this page_ before submitting a pull request. Thanks!

.. _page: http://binarytree.readthedocs.io/en/latest/contributing.html