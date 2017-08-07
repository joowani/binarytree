BinaryTree: Python Library for Learning Binary Trees
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

.. image:: https://user-images.githubusercontent.com/2701938/29019910-161f6cda-7b15-11e7-8bfb-49ea0a4179f9.gif
    :alt: Demo GIF

Introduction
============

Are you studying binary trees for your next exam, assignment or technical interview?

**BinaryTree** is a minimal Python library which gives you a simple API to
generate, visualize and inspect binary trees so you can skip the tedious
work of mocking up test objects and dive right into practising your algorithms!
Heaps and BSTs (binary search trees) are also supported.


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

By default, **BinaryTree** uses the following class to represent a tree node:

.. code-block:: python

    class Node(object):

        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None


Generate and pretty-print various types of binary trees:

.. code-block:: python

    from binarytree import tree, bst, heap, show

    # Generate a random binary tree and return its root
    my_tree = tree(height=5, is_balanced=False)

    # Generate a random binary search tree (BST) and return its root
    my_bst = bst(height=5)

    # Generate a random max heap and return its root
    my_heap = heap(height=3, is_max=True)

    # Pretty-print the trees in stdout
    show(my_tree)
    show(my_bst)
    show(my_heap)


`List representations`_ are supported as well:

.. _List representations:
    https://en.wikipedia.org/wiki/Binary_tree#Arrays


.. code-block:: python

    from heapq import heapify
    from binarytree import tree, convert, show

    my_list = [7, 3, 2, 6, 9, 4, 1, 5, 8]

    # Convert the list into a tree and return its root
    my_tree = convert(my_list)

    # Convert the list into a heap and return its root
    heapify(my_list)
    my_tree = convert(my_list)

    # Convert the tree back to a list
    my_list = convert(my_tree)

    # Pretty-printing also works on lists
    show(my_list)


Inspect a tree to quickly see its various properties:

.. code-block:: python

    from binarytree import tree, inspect

    my_tree = tree(height=10)

    result = inspect(my_tree)
    print(result['height'])
    print(result['node_count'])
    print(result['leaf_count'])
    print(result['min_value'])
    print(result['max_value'])
    print(result['min_leaf_depth'])
    print(result['max_leaf_depth'])
    print(result['is_bst'])
    print(result['is_max_heap'])
    print(result['is_min_heap'])
    print(result['is_height_balanced'])
    print(result['is_weight_balanced'])
    print(result['is_full'])


Use the `binarytree.Node` class to build your own trees:

.. code-block:: python

    from binarytree import Node, show

    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)

    show(root)


If the default `binarytree.Node` class does not meet your requirements, you can
define and use your own custom node specification:

.. code-block:: python

    from binarytree import Node, customize, tree, show

    # Define your own null/sentinel value
    my_null = -1

    # Define your own node class
    class MyNode(object):

        def __init__(self, data, left, right):
            self.data = data
            self.l_child = left
            self.r_child = right

    # Call customize in the beginning of your code to apply your specification
    customize(
        node_init=lambda val: MyNode(val, my_null, my_null),
        node_class=MyNode,
        null_value=my_null,
        value_attr='data',
        left_attr='l_child',
        right_attr='r_child'
    )
    my_custom_tree = tree()
    show(my_custom_tree)


**New in 2.0.0**: Utility functions you can play around with:

.. code-block:: python

    from binarytree import tree, show_ids, show_all, subtree, prune, leafs

    my_tree = tree(height=5, is_balanced=False)

    # Show the level-order node IDs instead of values
    show_ids(my_tree)

    # Show both the node IDs and the values
    show_all(my_tree)

    # Return the root of the subtree by its level-order ID
    subtree(my_tree, node_id=2)

    # Prune a node (and its children) by its level-order ID
    prune(my_tree, node_id=1)

    # Return the leaf nodes of the tree
    leafs(my_tree, values_only=True)


**New in 2.0.0**: The default `binarytree.Node` class comes with additional goodies:

.. code-block:: python

    from binarytree import tree

    my_tree = tree(height=5, is_balanced=False)

    # If you want to use these methods in your own custom class, your class
    # will have to inherit from the default binarytree.Node class
    my_tree.inspect()
    my_tree.show()
    my_tree.leafs()
    my_tree.subtree(node_id=2).show()
    my_tree.subtree(node_id=1).convert()
    my_tree.prune(node_id=1).show_all()
