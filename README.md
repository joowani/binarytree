# Binarytree: Python Library for Studying Binary Trees

## Introduction

Are you studying binary trees for your next exam, assignment or technical interview?

**Binarytree** is a Python library which provides a simple API to generate,
visualize, inspect and manipulate binary trees. It allows you to skip the
tedious work of setting up test data, and dive straight into practising your
algorithms. Heaps and BSTs (binary search trees) are also supported.

## Requirements

- Python 2.7, 3.4, 3.5 or 3.6.

## Installation

// TODO

## Getting started

By default, **binarytree** uses the following class to represent a node:

```python
class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value  # The node value
        self.left = left    # Left child
        self.right = right  # Right child
```

Use **Node** to build you trees:

```python
>>> from binarytree import Node
>>>
>>> root = Node(21)
>>> root.insert_node(4)
>>> root.insert_node(95)
>>> root.insert_node(17)
>>>
>>> print(root)

#    ___21
#   /     \
#  4       95
#   \
#    17

```

Inspect tree properties:

```python
>>> from binarytree import Node
>>>
>>> r = Node(4)
>>> r.insert_node(2)
>>> r.insert_node(1)
>>> r.insert_node(3)
>>> r.insert_node(5)
>>>
>>> print(root)

#      __4
#     /   \
#    2     5
#   / \
#  1   3

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
```

Use level-order indexes to manipulate nodes:

```python
>>> from binarytree import Node
>>>
>>> r = Node(4)
>>> r.insert_node(2)
>>> r.insert_node(1)
>>> r.insert_node(3)
>>> r.insert_node(5)
>>>
>>> print(root)

#      __4
#     /   \
#    2     5
#   / \
#  1   3

>>> # Use Node.pprint instead of print to display indexes
>>> root.pprint(index=True)

#         _____0-4_
#        /         \
#     _1-2_        2-5
#    /     \
#  3-1     4-3

>>> # Return the node/subtree at index 2
>>> root[2]
5

>>> # Replace the node/subtree at index 4
>>> root[4] = Node(6, left=Node(7), right=Node(8))
>>> root.pprint(index=True)

#         ______________0-4_
#        /                  \
#     _1-2_____             2-5
#    /         \
#  3-1        _4-6_
#            /     \
#          9-7     10-8

>>> # Delete the node/subtree at index 1
>>> del root[1]
>>> root.pprint(index=True)

#  0-4_
#      \
#      2-5

```

Traverse the trees using different algorithms:

```python
>>> from binarytree import Node
>>>
>>> r = Node(4)
>>> r.insert_node(2)
>>> r.insert_node(1)
>>> r.insert_node(3)
>>> r.insert_node(5)
>>>
>>> print(root)

#      __4
#     /   \
#    2     5
#   / \
#  1   3

>>> root.inorder
[Node(1), Node(2), Node(3), Node(4), Node(5)]

>>> root.preorder
[Node(4), Node(2), Node(1), Node(3), Node(5)]

>>> root.postorder
[Node(1), Node(3), Node(2), Node(5), Node(4)]

>>> root.levelorder
[Node(4), Node(2), Node(5), Node(1), Node(3)]

>>> list(root)  # Equivalent to root.levelorder
[Node(4), Node(2), Node(5), Node(1), Node(3)]
```
