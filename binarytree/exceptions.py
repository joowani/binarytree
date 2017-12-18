from __future__ import absolute_import, unicode_literals


class BinaryTreeError(Exception):
    """Base exception."""


class InvalidNodeValueError(BinaryTreeError):
    """Raised if a node has an invalid value."""


class InvalidNodeIndexError(BinaryTreeError):
    """Raised if an invalid level-order index is given."""


class InvalidNodeTypeError(BinaryTreeError):
    """Raised if a node is not an instance of :class:`binarytree.Node`."""


class OperationForbiddenError(BinaryTreeError):
    """Raised if the user tries to overwrite or delete the root node."""


class NodeNotFoundError(BinaryTreeError):
    """Raised if a node is missing from the binary tree."""


class InvalidTreeHeightError(BinaryTreeError):
    """Raised if an invalid tree height is given."""


class CyclicNodeReferenceError(BinaryTreeError):
    """Raised if the binary tree has a cyclic reference to a node."""
