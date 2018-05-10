from __future__ import absolute_import, unicode_literals


class BinaryTreeError(Exception):
    """Base (catch-all) binarytree exception."""


class NodeIndexError(BinaryTreeError):
    """Node index was invalid."""


class NodeModifyError(BinaryTreeError):
    """User tried to overwrite or delete the root node."""


class NodeNotFoundError(BinaryTreeError):
    """Node was missing from the binary tree."""


class NodeReferenceError(BinaryTreeError):
    """Node reference was invalid (e.g. cyclic reference)."""


class NodeTypeError(BinaryTreeError):
    """Node was not an instance of :class:`binarytree.Node`."""


class NodeValueError(BinaryTreeError):
    """Node value was not a number (e.g. int, float)."""


class TreeHeightError(BinaryTreeError):
    """Tree height was invalid."""
