from __future__ import absolute_import, unicode_literals, division

__all__ = ['Node', 'tree', 'bst', 'heap', 'build']

import heapq
import random

from binarytree.exceptions import (
    InvalidNodeValueError,
    InvalidNodeIndexError,
    InvalidNodeTypeError,
    OperationForbiddenError,
    NodeNotFoundError,
    InvalidTreeHeightError,
    CyclicNodeReferenceError,
)


def _is_balanced(root):
    """Return the height if the binary tree is balanced, -1 otherwise.

    :param root: The root node of the binary tree.
    :type root: binarytree.Node | None
    :return: The height or -1.
    :rtype: int
    """
    if root is None:
        return 0
    left = _is_balanced(root.left)
    if left < 0:
        return -1
    right = _is_balanced(root.right)
    if right < 0:
        return -1
    return -1 if abs(left - right) > 1 else max(left, right) + 1


def _is_bst(root, min_value=float('-inf'), max_value=float('inf')):
    """Check if the binary tree is a BST (binary search tree).

    :param root: The root node of the binary tree.
    :type root: binarytree.Node | None
    :param min_value: The minimum node value seen.
    :type min_value: int | float
    :param max_value: The maximum node value seen.
    :type max_value: int | float
    :return: True if the binary tree is a BST, False otherwise.
    :rtype: bool
    """
    if root is None:
        return True
    return (
        min_value < root.value < max_value and
        _is_bst(root.left, min_value, root.value) and
        _is_bst(root.right, root.value, max_value)
    )


def _validate_tree_height(height):
    """Check if the height of the binary tree is valid.

    :param height: The height of the binary tree (must be 0 - 9 inclusive).
    :type height: int
    :raise binarytree.exceptions.InvalidTreeHeightError:
        If an invalid tree height is given.
    """
    if not (isinstance(height, int) and 0 <= height <= 9):
        raise InvalidTreeHeightError(
            'The height must be an integer between 0 - 9'
        )


def _generate_perfect_bst(height):
    """Generate a perfect BST (binary search tree) and return its root node.

    :param height: The height of the binary tree to build.
    :type height: int
    :return: The root node of the BST.
    :rtype: binarytree.Node
    """
    max_node_count = 2 ** (height + 1) - 1
    node_values = list(range(max_node_count))
    return _build_bst_from_sorted_values(node_values)


def _build_bst_from_sorted_values(sorted_values):
    """Recursively build a perfect BST from odd number of sorted values.

    :param sorted_values: Odd number of sorted values.
    :type sorted_values: [int]
    :return: The root node of the BST.
    :rtype: binarytree.Node
    """
    if len(sorted_values) == 0:
        return None
    mid_index = len(sorted_values) // 2
    root = Node(sorted_values[mid_index])
    root.left = _build_bst_from_sorted_values(sorted_values[:mid_index])
    root.right = _build_bst_from_sorted_values(sorted_values[mid_index + 1:])
    return root


def _generate_random_leaf_count(height):
    """Return a random leaf count for building binary trees.

    :param height: The height of the binary tree to build.
    :type height: int
    :return: Randomly generated leaf count.
    :rtype: int
    """
    max_leaf_count = 2 ** height
    half_leaf_count = max_leaf_count // 2

    # A very naive way of mimicking normal distribution
    roll_1 = random.randint(0, half_leaf_count)
    roll_2 = random.randint(0, max_leaf_count - half_leaf_count)
    return roll_1 + roll_2 or half_leaf_count


def _generate_random_node_values(height):
    """Return random node values for building binary trees.

    :param height: The height of the binary tree to build.
    :type height: int
    :return: Randomly generated node values.
    :rtype: [int]
    """
    max_node_count = 2 ** (height + 1) - 1
    node_values = list(range(max_node_count))
    random.shuffle(node_values)
    return node_values


def _build_tree_string(root, curr_index, index=False, delimiter='-'):
    """Recursively traverse down the binary tree build a pretty-print string.

    In each recursive call, a "box" of characters visually representing the
    current (sub)tree is constructed line by line. Each line is padded with
    whitespaces to ensure all lines in the box have the same length. Then the
    box, its width, and start-end positions of its root value repr (required
    for drawing branches) are sent up to the parent call. The parent call then
    combines its left and right sub-boxes to construct a larger box etc.

    :param root: The root node of the binary tree.
    :type root: binarytree.Node | None
    :param curr_index: The level-order_ index of the current node (root is 0).
    :type curr_index: int
    :param index: If set to True, include the level-order_ node indexes
        using the following format: ``{index}{delimiter}{value}``
        (default: False).
    :type index: bool
    :param delimiter: The delimiter character between the node index and value
        (default: '-').
    :type delimiter:
    :return: The box of characters visually representing the current subtree,
        the width of the box, and the start-end positions of the new root value
        repr string.
    :rtype: ([str], int, int, int)

    .. _level-order:
        https://en.wikipedia.org/wiki/Tree_traversal
    """
    if root is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    if index:
        node_repr = '{}{}{}'.format(curr_index, delimiter, root.value)
    else:
        node_repr = str(root.value)

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = \
        _build_tree_string(root.left, 2 * curr_index + 1, index, delimiter)
    r_box, r_box_width, r_root_start, r_root_end = \
        _build_tree_string(root.right, 2 * curr_index + 2, index, delimiter)

    # Draw the branch connecting the current root to the left sub-box
    # Pad with whitespaces where necessary
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(' ' * (l_root + 1))
        line1.append('_' * (l_box_width - l_root))
        line2.append(' ' * l_root + '/')
        line2.append(' ' * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root
    line1.append(node_repr)
    line2.append(' ' * new_root_width)

    # Draw the branch connecting the current root to the right sub-box
    # Pad with whitespaces where necessary
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append('_' * r_root)
        line1.append(' ' * (r_box_width - r_root + 1))
        line2.append(' ' * r_root + '\\')
        line2.append(' ' * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    gap = ' ' * gap_size
    new_box = [''.join(line1), ''.join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
        r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root positions
    return new_box, len(new_box[0]), new_root_start, new_root_end


def _get_tree_properties(root):
    """Inspect the binary tree and return its properties (e.g. height).

    :param root: The root node of the binary tree.
    :rtype: binarytree.Node
    :return: The properties of the binary tree.
    :rtype: dict
    """
    is_descending = True
    is_ascending = True
    min_node_value = root.value
    max_node_value = root.value
    size = 0
    leaf_count = 0
    min_leaf_depth = 0
    max_leaf_depth = -1
    is_strict = True
    is_complete = True
    current_nodes = [root]
    non_full_node_seen = False

    while len(current_nodes) > 0:
        max_leaf_depth += 1
        next_nodes = []

        for node in current_nodes:
            size += 1
            value = node.value
            min_node_value = min(value, min_node_value)
            max_node_value = max(value, max_node_value)

            # The node is a leaf.
            if node.left is None and node.right is None:
                if min_leaf_depth == 0:
                    min_leaf_depth = max_leaf_depth
                leaf_count += 1

            if node.left is not None:
                if node.left.value > value:
                    is_descending = False
                elif node.left.value < value:
                    is_ascending = False
                next_nodes.append(node.left)
                is_complete = not non_full_node_seen
            else:
                non_full_node_seen = True

            if node.right is not None:
                if node.right.value > value:
                    is_descending = False
                elif node.right.value < value:
                    is_ascending = False
                next_nodes.append(node.right)
                is_complete = not non_full_node_seen
            else:
                non_full_node_seen = True

            # If we see a node with only one child, it is not strict
            is_strict &= (node.left is None) == (node.right is None)

        current_nodes = next_nodes

    return {
        'height': max_leaf_depth,
        'size': size,
        'is_max_heap': is_complete and is_descending,
        'is_min_heap': is_complete and is_ascending,
        'is_perfect': leaf_count == 2 ** max_leaf_depth,
        'is_strict': is_strict,
        'is_complete': is_complete,
        'leaf_count': leaf_count,
        'min_node_value': min_node_value,
        'max_node_value': max_node_value,
        'min_leaf_depth': min_leaf_depth,
        'max_leaf_depth': max_leaf_depth,
    }


class Node(object):
    """Represents a binary tree node.

    This class provides methods and properties for managing the calling node,
    and the binary tree which the calling node is the root of. Whenever a
    docstring in this class says "binary tree", it is referring to the calling
    node instance and its descendants.

    :param value: The node value. Only integers are supported.
    :type value: int
    :param left: The left child node (default: None).
    :type left: binarytree.Node | None
    :param right: The right child node (default: None).
    :type right: binarytree.Node | None
    :raise binarytree.exceptions.InvalidNodeValueError:
        If the node value is not an integer.
    :raise binarytree.exceptions.InvalidNodeTypeError:
        If the left or right child is not an instance of
        :class:`binarytree.Node`.
    """

    def __init__(self, value, left=None, right=None):
        if not isinstance(value, int):
            raise InvalidNodeValueError('The node value must be an integer')
        if left is not None and not isinstance(left, Node):
            raise InvalidNodeTypeError(
                'The left child node is not a binarytree.Node instance')
        if right is not None and not isinstance(right, Node):
            raise InvalidNodeTypeError(
                'The right child node is not a binarytree.Node instance')

        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        """Return the string representation of the node.

        :return: The string representation.
        :rtype: str | unicode

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> Node(1)
            Node(1)
        """
        return 'Node({})'.format(self.value)

    def __str__(self):
        """Return the pretty-print string for the binary tree.

        :return: The pretty-print string.
        :rtype: str | unicode

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.right = Node(4)
            >>>
            >>> print(root)
            <BLANKLINE>
              __1
             /   \\
            2     3
             \\
              4
            <BLANKLINE>

        .. note::

            To include `level-order (breadth-first)`_ indexes in the string, use
            :func:`binarytree.Node.pprint` instead.

        .. _level-order (breadth-first):
            https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search
        """
        lines = _build_tree_string(self, 0, False, '-')[0]
        return '\n' + '\n'.join((line.rstrip() for line in lines))

    def __setattr__(self, attribute, obj):
        """Modified version of **__setattr__** with extra sanity checks
        around class attributes **left**, **right** and **value**.

        :param attribute: The name of the class attribute.
        :type attribute: str | unicode
        :param obj: The object to set.
        :type obj: object
        :raise binarytree.exceptions.InvalidNodeTypeError:
            If the left or right child is not an instance of
            :class:`binarytree.Node`.
        :raise binarytree.exceptions.InvalidNodeValueError:
            If the node value is not an integer.

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> node = Node(1)
            >>> node.left = 'invalid'  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
             ...
            InvalidNodeTypeError: The node is not a binarytree.Node instance

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> node = Node(1)
            >>> node.value = 'invalid'  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
             ...
            InvalidNodeValueError: The node value must be an integer
        """
        if attribute == 'left' or attribute == 'right':
            if obj is not None and not isinstance(obj, Node):
                raise InvalidNodeTypeError(
                    'The node is not a binarytree.Node instance')
        elif attribute == 'value' and not isinstance(obj, int):
            raise InvalidNodeValueError('The node value must be an integer')
        object.__setattr__(self, attribute, obj)

    def __iter__(self):
        """Return the `list representation`_ of the binary tree.

        .. _list representation:
            https://en.wikipedia.org/wiki/Binary_tree#Arrays

        :return: The list representation consisting of node values or None's.
            If a node has an index i, its left child is at index 2i + 1, right
            child at index 2i + 2, and parent at index floor((i - 1) / 2). None
            signifies the absence of a node. See example below for an
            illustration.
        :rtype: [int | None]

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.right = Node(4)
            >>>
            >>> list(root)
            [1, 2, 3, None, 4]
        """
        current_nodes = [self]
        has_more_nodes = True
        values = []

        while has_more_nodes:
            has_more_nodes = False
            next_nodes = []
            for node in current_nodes:
                if node is None:
                    values.append(None)
                    next_nodes.extend((None, None))
                    continue

                if node.left is not None or node.right is not None:
                    has_more_nodes = True

                values.append(node.value)
                next_nodes.extend((node.left, node.right))

            current_nodes = next_nodes

        # Get rid of the trailing None entries
        while values and values[-1] is None:
            values.pop()

        return iter(values)

    def __len__(self):
        """Return the total number of nodes in the binary tree.

        :return: The total number of nodes.
        :rtype: int

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>>
            >>> len(root)
            3

        .. note::

            This method is equivalent to :attr:`binarytree.Node.size`.
        """
        return self.properties['size']

    def __getitem__(self, index):
        """Return the node/subtree at the give `level-order (breadth-first)`_
        index.

        :param index: The node index.
        :type index: int
        :return: The node at the given index.
        :rtype: binarytree.Node
        :raise binarytree.exceptions.InvalidNodeIndexError:
            If an invalid index is given.
        :raise binarytree.exceptions.NodeNotFoundError:
            If the target node does not exist.

        .. _level-order (breadth-first):
            https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)       # index: 0, value: 1
            >>> root.left = Node(2)  # index: 1, value: 2
            >>> root.right = Node(3) # index: 2, value: 3
            >>>
            >>> root[0]
            Node(1)
            >>> root[1]
            Node(2)
            >>> root[2]
            Node(3)
            >>> root[3]  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
             ...
            NodeNotFoundError: Node missing at index 3
        """
        if not isinstance(index, int) or index < 0:
            raise InvalidNodeIndexError(
                'The node index must be a non-negative integer')

        current_nodes = [self]
        current_index = 0
        has_more_nodes = True

        while has_more_nodes:
            has_more_nodes = False
            next_nodes = []

            for node in current_nodes:
                if current_index == index:
                    if node is None:
                        break
                    else:
                        return node
                current_index += 1

                if node is None:
                    next_nodes.extend((None, None))
                    continue
                next_nodes.extend((node.left, node.right))
                if node.left is not None or node.right is not None:
                    has_more_nodes = True

            current_nodes = next_nodes

        raise NodeNotFoundError('Node missing at index {}'.format(index))

    def __setitem__(self, index, node):
        """Insert the node/subtree into the binary tree at the given
        `level-order (breadth-first)`_ index.

        * An exception is raised if the parent node does not exist.
        * Any existing node/subtree is overwritten.
        * The root node (calling node) cannot be replaced.

        :param index: The node index.
        :type index: int
        :param node: The new node to insert.
        :type node: binarytree.Node
        :raise binarytree.exceptions.OperationForbiddenError:
            If the user tries to overwrite the root node (calling node).
        :raise binarytree.exceptions.NodeNotFoundError:
            If the parent for the new node does not exist.
        :raise binarytree.exceptions.InvalidNodeTypeError:
            If the new node is not an instance of :class:`binarytree.Node`.

        .. _level-order (breadth-first):
            https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)       # index: 0, value: 1
            >>> root.left = Node(2)  # index: 1, value: 2
            >>> root.right = Node(3) # index: 2, value: 3
            >>>
            >>> root[0] = Node(4)  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
             ...
            OperationForbiddenError: Cannot modify the root node

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)       # index: 0, value: 1
            >>> root.left = Node(2)  # index: 1, value: 2
            >>> root.right = Node(3) # index: 2, value: 3
            >>>
            >>> root[11] = Node(4)  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
             ...
            NodeNotFoundError: Parent node missing at index 5

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)       # index: 0, value: 1
            >>> root.left = Node(2)  # index: 1, value: 2
            >>> root.right = Node(3) # index: 2, value: 3
            >>>
            >>> root[1] = Node(4)
            >>>
            >>> root.left
            Node(4)
        """
        if index == 0:
            raise OperationForbiddenError('Cannot modify the root node')

        parent_index = (index - 1) // 2
        try:
            parent = self.__getitem__(parent_index)
        except NodeNotFoundError:
            raise NodeNotFoundError(
                'Parent node missing at index {}'.format(parent_index))
        setattr(parent, 'left' if index % 2 else 'right', node)

    def __delitem__(self, index):
        """Remove the node/subtree at the given `level-order (breadth-first)`_
        index from the binary tree.

        * An exception is raised if the target node does not exist.
        * The descendants of the target node (if any) are also removed.
        * The root node (calling node) cannot be deleted.

        :param index: The node index.
        :type index: int
        :raise binarytree.exceptions.OperationForbiddenError:
            If the user tries to delete the root node (calling node).
        :raise binarytree.exceptions.NodeNotFoundError:
            If the target node or its parent does not exist.

        .. _level-order (breadth-first):
            https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)          # index: 0, value: 1
            >>> root.left = Node(2)     # index: 1, value: 2
            >>> root.right = Node(3)    # index: 2, value: 3
            >>>
            >>> del root[0]  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
             ...
            OperationForbiddenError: Cannot delete the root node

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)          # index: 0, value: 1
            >>> root.left = Node(2)     # index: 1, value: 2
            >>> root.right = Node(3)    # index: 2, value: 3
            >>>
            >>> del root[2]
            >>>
            >>> root[2]  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
             ...
            NodeNotFoundError: Node missing at index 2
        """
        if index == 0:
            raise OperationForbiddenError('Cannot delete the root node')

        parent_index = (index - 1) // 2
        try:
            parent = self.__getitem__(parent_index)
        except NodeNotFoundError:
            raise NodeNotFoundError(
                'No node to delete at index {}'.format(index))

        child_attr = 'left' if index % 2 == 1 else 'right'
        if getattr(parent, child_attr) is None:
            raise NodeNotFoundError(
                'No node to delete at index {}'.format(index))
        setattr(parent, child_attr, None)

    def pprint(self, index=False, delimiter='-'):
        """Pretty-print the binary tree.

        :param index: If set to True (default: False), display the
            `level-order (breadth-first)`_ indexes using the following
            format: "{index}{delimiter}{value}".
        :type index: bool
        :param delimiter: The delimiter character between the node index, and
            the node value (default: "-").
        :type delimiter: str | unicode

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)              # index: 0, value: 1
            >>> root.left = Node(2)         # index: 1, value: 2
            >>> root.right = Node(3)        # index: 2, value: 3
            >>> root.left.right = Node(4)   # index: 4, value: 4
            >>>
            >>> root.pprint()
            <BLANKLINE>
              __1
             /   \\
            2     3
             \\
              4
            <BLANKLINE>
            >>> root.pprint(index=True)      # Format: {index}-{value}
            <BLANKLINE>
               _____0-1_
              /         \\
            1-2_        2-3
                \\
                4-4
            <BLANKLINE>

        .. note::
            If you don't need to see the node indexes, you can use
            :func:`binarytree.Node.__str__`.
        """
        lines = _build_tree_string(self, 0, index, delimiter)[0]
        print('\n' + '\n'.join((line.rstrip() for line in lines)))

    def validate(self):
        """Check if the binary tree is malformed.

        :raise binarytree.exceptions.CyclicNodeReferenceError:
            If there is a cyclic reference to a node in the binary tree.
        :raise binarytree.exceptions.InvalidNodeTypeError:
            If a node is not an instance of :class:`binarytree.Node`.
        :raise binarytree.exceptions.InvalidNodeValueError:
            If a node value is not an integer.

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = root  # Cyclic reference to root
            >>>
            >>> root.validate()  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
             ...
            CyclicNodeReferenceError: Cyclic node reference at index 0
        """
        has_more_nodes = True
        nodes_visited = set()
        current_nodes = [self]
        current_index = 0

        while has_more_nodes:
            has_more_nodes = False
            next_nodes = []

            for node in current_nodes:
                if node is None:
                    next_nodes.extend((None, None))
                else:
                    if node in nodes_visited:
                        raise CyclicNodeReferenceError(
                            'Cyclic node reference at index {}'
                            .format(current_index)
                        )
                    if not isinstance(node, Node):
                        raise InvalidNodeTypeError(
                            'Invalid node instance at index {}'
                            .format(current_index)
                        )
                    if not isinstance(node.value, int):
                        raise InvalidNodeValueError(
                            'Invalid node value at index {}'
                            .format(current_index)
                        )
                    if node.left is not None or node.right is not None:
                        has_more_nodes = True
                    nodes_visited.add(node)
                    next_nodes.extend((node.left, node.right))
                current_index += 1

            current_nodes = next_nodes

    @property
    def leaves(self):
        """Return the leaves of the binary tree.

        :return: The list of leaf nodes.
        :rtype: [binarytree.Node]

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.right = Node(4)
            >>>
            >>> print(root)
            <BLANKLINE>
              __1
             /   \\
            2     3
             \\
              4
            <BLANKLINE>
            >>> root.leaves
            [Node(3), Node(4)]
        """
        current_nodes = [self]
        leaves = []

        while len(current_nodes) > 0:
            next_nodes = []
            for node in current_nodes:
                if node.left is None and node.right is None:
                    leaves.append(node)
                    continue
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            current_nodes = next_nodes
        return leaves

    @property
    def levels(self):
        """Return the nodes in the binary tree level by level.

        :return: The per-level lists of nodes.
        :rtype: [[binarytree.Node]]

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.right = Node(4)
            >>>
            >>> print(root)
            <BLANKLINE>
              __1
             /   \\
            2     3
             \\
              4
            <BLANKLINE>
            >>>
            >>> root.levels
            [[Node(1)], [Node(2), Node(3)], [Node(4)]]
        """
        current_nodes = [self]
        levels = []

        while len(current_nodes) > 0:
            next_nodes = []
            for node in current_nodes:
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            levels.append(current_nodes)
            current_nodes = next_nodes
        return levels

    @property
    def height(self):
        """Return the height of the binary tree.

        :return: The height of the binary tree.
        :rtype: int

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.left.left = Node(3)
            >>>
            >>> print(root)
            <BLANKLINE>
                1
               /
              2
             /
            3
            <BLANKLINE>
            >>> root.height
            2

        .. note::

            A binary tree with only a root node has a height of 0.
        """
        return _get_tree_properties(self)['height']

    @property
    def size(self):
        """Return the total number of nodes in the binary tree.

        :return: The total number of nodes.
        :rtype: int

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.right = Node(4)
            >>>
            >>> root.size
            4

        .. note::

            This method is equivalent to :func:`binarytree.Node.__len__`.
        """
        return _get_tree_properties(self)['size']

    @property
    def leaf_count(self):
        """Return the total number of leaves in the binary tree.

        :return: The total number of leaves.
        :rtype: int

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.right = Node(4)
            >>>
            >>> root.leaf_count
            2
        """
        return _get_tree_properties(self)['leaf_count']

    @property
    def is_balanced(self):
        """Return True if the binary tree is height-balanced, False otherwise.

        :return: True if the binary tree is balanced, False otherwise.
        :rtype: bool

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.left.left = Node(3)
            >>>
            >>> print(root)
            <BLANKLINE>
                1
               /
              2
             /
            3
            <BLANKLINE>
            >>> root.is_balanced
            False
        """
        return _is_balanced(self) >= 0

    @property
    def is_bst(self):
        """Return True if the binary tree is a BST (binary search tree),
        False otherwise.

        :return: True if the binary tree is a BST, False otherwise.
        :rtype: bool

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(2)
            >>> root.left = Node(1)
            >>> root.right = Node(3)
            >>>
            >>> print(root)
            <BLANKLINE>
              2
             / \\
            1   3
            <BLANKLINE>
            >>> root.is_bst
            True
        """
        return _is_bst(self, float('-inf'), float('inf'))

    @property
    def is_max_heap(self):
        """Return True if the binary tree is a max heap, False otherwise.

        :return: True if the binary tree is a max heap, False otherwise.
        :rtype: bool

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(3)
            >>> root.left = Node(1)
            >>> root.right = Node(2)
            >>>
            >>> print(root)
            <BLANKLINE>
              3
             / \\
            1   2
            <BLANKLINE>
            >>> root.is_max_heap
            True
        """
        return _get_tree_properties(self)['is_max_heap']

    @property
    def is_min_heap(self):
        """Return True if the binary tree is a min heap, False otherwise.

        :return: True if the binary tree is a min heap, False otherwise.
        :rtype: bool

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>>
            >>> print(root)
            <BLANKLINE>
              1
             / \\
            2   3
            <BLANKLINE>
            >>> root.is_min_heap
            True
        """
        return _get_tree_properties(self)['is_min_heap']

    @property
    def is_perfect(self):
        """Return True if the binary tree is perfect (i.e. all levels are
        completely filled), False otherwise.

        :return: True if the binary tree is perfect, False otherwise.
        :rtype: bool

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.left = Node(4)
            >>> root.left.right = Node(5)
            >>> root.right.left = Node(6)
            >>> root.right.right = Node(7)
            >>>
            >>> print(root)
            <BLANKLINE>
                __1__
               /     \\
              2       3
             / \\     / \\
            4   5   6   7
            <BLANKLINE>
            >>> root.is_perfect
            True
        """
        return _get_tree_properties(self)['is_perfect']

    @property
    def is_strict(self):
        """Return True if the binary tree is strict (i.e. all non-leaf nodes
        have both children), False otherwise.

        :return: True if the binary tree is strict, False otherwise.
        :rtype: bool

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.left = Node(4)
            >>> root.left.right = Node(5)
            >>>
            >>> print(root)
            <BLANKLINE>
                __1
               /   \\
              2     3
             / \\
            4   5
            <BLANKLINE>
            >>> root.is_strict
            True

        .. note::

            Strictly binary nodes are also called **full** nodes.
        """
        return _get_tree_properties(self)['is_strict']

    @property
    def is_complete(self):
        """Return True if the binary tree is complete (i.e. all levels except
        possibly the last are completely filled, and the last level is always
        left-justified), False otherwise.

        :return: True if the binary tree is complete, False otherwise.
        :rtype: bool

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.left = Node(4)
            >>> root.left.right = Node(5)
            >>>
            >>> print(root)
            <BLANKLINE>
                __1
               /   \\
              2     3
             / \\
            4   5
            <BLANKLINE>
            >>> root.is_complete
            True
        """
        return _get_tree_properties(self)['is_complete']

    @property
    def min_node_value(self):
        """Return the minimum node value in the binary tree.

        :return: The minimum node value.
        :rtype: int

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>>
            >>> root.min_node_value
            1
        """
        return _get_tree_properties(self)['min_node_value']

    @property
    def max_node_value(self):
        """Return the maximum node value in the binary tree.

        :return: The maximum node value.
        :rtype: int

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>>
            >>> root.max_node_value
            3
        """
        return _get_tree_properties(self)['max_node_value']

    @property
    def max_leaf_depth(self):
        """Return the maximum leaf node depth in the binary tree.

        :return: The maximum leaf node depth.
        :rtype: int

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.right.left = Node(4)
            >>> root.right.left.left = Node(5)
            >>>
            >>> print(root)
            <BLANKLINE>
              1____
             /     \\
            2       3
                   /
                  4
                 /
                5
            <BLANKLINE>
            >>> root.max_leaf_depth
            3
        """
        return _get_tree_properties(self)['max_leaf_depth']

    @property
    def min_leaf_depth(self):
        """Return the minimum leaf node depth in the binary tree.

        :return: The minimum leaf node depth.
        :rtype: int

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.right.left = Node(4)
            >>> root.right.left.left = Node(5)
            >>>
            >>> print(root)
            <BLANKLINE>
              1____
             /     \\
            2       3
                   /
                  4
                 /
                5
            <BLANKLINE>
            >>> root.min_leaf_depth
            1
        """
        return _get_tree_properties(self)['min_leaf_depth']

    @property
    def properties(self):
        """Return various properties of the the binary tree all at once.

        :return: The properties of the binary tree.
        :rtype: dict

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.left = Node(4)
            >>> root.left.right = Node(5)
            >>> props = root.properties
            >>>
            >>> props['height']         # equivalent to root.height
            2
            >>> props['size']           # equivalent to root.size
            5
            >>> props['max_leaf_depth'] # equivalent to root.max_leaf_depth
            2
            >>> props['min_leaf_depth'] # equivalent to root.min_leaf_depth
            1
            >>> props['max_node_value'] # equivalent to root.max_node_value
            5
            >>> props['min_node_value'] # equivalent to root.min_node_value
            1
            >>> props['leaf_count']     # equivalent to root.leaf_count
            3
            >>> props['is_balanced']    # equivalent to root.is_balanced
            True
            >>> props['is_bst']         # equivalent to root.is_bst
            False
            >>> props['is_complete']    # equivalent to root.is_complete
            True
            >>> props['is_max_heap']    # equivalent to root.is_max_heap
            False
            >>> props['is_min_heap']    # equivalent to root.is_min_heap
            True
            >>> props['is_perfect']     # equivalent to root.is_perfect
            False
            >>> props['is_strict']      # equivalent to root.is_strict
            True
        """
        properties = _get_tree_properties(self)
        properties.update({
            'is_bst': _is_bst(self),
            'is_balanced': _is_balanced(self) >= 0
        })
        return properties

    @property
    def inorder(self):
        """Return the nodes in the binary tree using in-order_ (left, root,
        right) traversal.

        .. _in-order:
            https://en.wikipedia.org/wiki/Tree_traversal

        :return: The list of nodes.
        :rtype: [binarytree.Node]

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.left = Node(4)
            >>> root.left.right = Node(5)
            >>>
            >>> print(root)
            <BLANKLINE>
                __1
               /   \\
              2     3
             / \\
            4   5
            <BLANKLINE>
            >>> root.inorder
            [Node(4), Node(2), Node(5), Node(1), Node(3)]
        """
        node_stack = []
        result = []
        node = self

        while True:
            if node is not None:
                node_stack.append(node)
                node = node.left
            elif len(node_stack) > 0:
                node = node_stack.pop()
                result.append(node)
                node = node.right
            else:
                break

        return result

    @property
    def preorder(self):
        """Return the nodes in the binary tree using pre-order_ (root, left,
        right) traversal.

        .. _pre-order:
            https://en.wikipedia.org/wiki/Tree_traversal

        :return: The list of nodes.
        :rtype: [binarytree.Node]

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.left = Node(4)
            >>> root.left.right = Node(5)
            >>>
            >>> print(root)
            <BLANKLINE>
                __1
               /   \\
              2     3
             / \\
            4   5
            <BLANKLINE>
            >>> root.preorder
            [Node(1), Node(2), Node(4), Node(5), Node(3)]
        """
        node_values = []
        node_stack = [self]

        while len(node_stack) > 0:
            node = node_stack.pop()
            node_values.append(node)

            if node.right is not None:
                node_stack.append(node.right)
            if node.left is not None:
                node_stack.append(node.left)

        return node_values

    @property
    def postorder(self):
        """Return the nodes in the binary tree using post-order_ (left, right,
        root) traversal.

        .. _post-order:
            https://en.wikipedia.org/wiki/Tree_traversal

        :return: The list of nodes.
        :rtype: [binarytree.Node]


        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.left = Node(4)
            >>> root.left.right = Node(5)
            >>>
            >>> print(root)
            <BLANKLINE>
                __1
               /   \\
              2     3
             / \\
            4   5
            <BLANKLINE>
            >>> root.postorder
            [Node(4), Node(5), Node(2), Node(3), Node(1)]
        """
        node_values = []
        node_stack = []
        node = self

        while True:
            while node is not None:
                if node.right is not None:
                    node_stack.append(node.right)
                node_stack.append(node)
                node = node.left

            node = node_stack.pop()
            if (node.right is not None and
                    len(node_stack) > 0 and
                    node_stack[-1] is node.right):
                node_stack.pop()
                node_stack.append(node)
                node = node.right
            else:
                node_values.append(node)
                node = None

            if len(node_stack) == 0:
                break

        return node_values

    @property
    def levelorder(self):
        """Return the nodes in the binary tree using
        `level-order (breadth-first)`_ traversal.

        .. _level-order (breadth-first):
            https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search

        :return: The list of nodes.
        :rtype: [binarytree.Node]

        **Example**:

        .. doctest::

            >>> from binarytree import Node
            >>>
            >>> root = Node(1)
            >>> root.left = Node(2)
            >>> root.right = Node(3)
            >>> root.left.left = Node(4)
            >>> root.left.right = Node(5)
            >>>
            >>> print(root)
            <BLANKLINE>
                __1
               /   \\
              2     3
             / \\
            4   5
            <BLANKLINE>
            >>> root.levelorder
            [Node(1), Node(2), Node(3), Node(4), Node(5)]
        """
        current_nodes = [self]
        node_values = []

        while len(current_nodes) > 0:
            next_nodes = []
            for node in current_nodes:
                node_values.append(node)
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            current_nodes = next_nodes

        return node_values


def build(values):
    """Build a binary tree from a `list representation`_ (i.e. a list of
    node values and/or None's in breadth-first order) and return its root.

    :param values: The list representation (i.e. a list of node values and/or
        None's in breadth-first order). If a node has an index i, its left child
        is at index 2i + 1, right child at index 2i + 2, and parent at index
        floor((i - 1) / 2). None signifies the absence of a node. See example
        below for an illustration.
    :type values: [int | None]
    :return: The root of the binary tree.
    :rtype: binarytree.Node
    :raise binarytree.exceptions.NodeNotFoundError:
        If the list representation is malformed and a parent node is missing.

    .. _list representation:
        https://en.wikipedia.org/wiki/Binary_tree#Arrays

    **Example**:

    .. doctest::

        >>> from binarytree import build
        >>>
        >>> root = build([1, 2, 3, None, 4])
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>

    .. doctest::

        >>> from binarytree import build
        >>>
        >>> root = build([None, 2, 3])  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
         ...
        NodeNotFoundError: Parent node missing at index 0
    """
    nodes = [None if v is None else Node(v) for v in values]

    for index in range(1, len(nodes)):
        node = nodes[index]
        if node is not None:
            parent_index = (index - 1) // 2
            parent = nodes[parent_index]
            if parent is None:
                raise NodeNotFoundError(
                    'Parent node missing at index {}'
                    .format(parent_index)
                )
            setattr(parent, 'left' if index % 2 else 'right', node)

    return nodes[0] if nodes else None


def tree(height=3, is_perfect=False):
    """Generate a random binary tree and return its root node.

    :param height: The height of the tree (default: 3, range: 0 - 9 inclusive).
    :type height: int
    :param is_perfect: If set to True (default: False), a perfect binary tree
        with all levels filled is returned. When set to False, a perfect binary
        tree may still be generated and returned by chance.
    :type is_perfect: bool
    :return: The root node of the generated tree.
    :rtype: binarytree.Node
    :raise binarytree.exceptions.InvalidTreeHeightError:
        If an invalid tree height is given.

    **Example**:

    .. doctest::

        >>> from binarytree import tree
        >>>
        >>> root = tree()
        >>>
        >>> root.height
        3

    .. doctest::

        >>> from binarytree import tree
        >>>
        >>> root = tree(height=5, is_perfect=True)
        >>>
        >>> root.height
        5
        >>> root.is_perfect
        True

    .. doctest::

        >>> from binarytree import tree
        >>>
        >>> root = tree(height=20)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
         ...
        InvalidTreeHeightError: The height must be an integer between 0 - 9
    """
    _validate_tree_height(height)
    values = _generate_random_node_values(height)
    if is_perfect:
        return build(values)

    leaf_count = _generate_random_leaf_count(height)
    root = Node(values.pop(0))
    leaves = set()

    for value in values:
        node = root
        depth = 0
        inserted = False

        while depth < height and not inserted:
            attr = random.choice(('left', 'right'))
            if getattr(node, attr) is None:
                setattr(node, attr, Node(value))
                inserted = True
            node = getattr(node, attr)
            depth += 1

        if inserted and depth == height:
            leaves.add(node)
        if len(leaves) == leaf_count:
            break

    return root


def bst(height=3, is_perfect=False):
    """Generate a random BST (binary search tree) and return its root node.

    :param height: The height of the BST (default: 3, range: 0 - 9 inclusive).
    :type height: int
    :param is_perfect: If set to True (default: False), a perfect BST with all
        levels filled is returned. When set to False, a perfect BST may still
        be generated and returned by chance.
    :type is_perfect: bool
    :return: The root node of the generated BST.
    :rtype: binarytree.Node
    :raise binarytree.exceptions.InvalidTreeHeightError:
        If an invalid tree height is given.

    **Example**:

    .. doctest::

        >>> from binarytree import bst
        >>>
        >>> root = bst()
        >>>
        >>> root.height
        3
        >>> root.is_bst
        True

    .. doctest::

        >>> from binarytree import bst
        >>>
        >>> root = bst(10)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
         ...
        InvalidTreeHeightError: The height must be an integer between 0 - 9
    """
    _validate_tree_height(height)
    if is_perfect:
        return _generate_perfect_bst(height)

    values = _generate_random_node_values(height)
    leaf_count = _generate_random_leaf_count(height)

    root = Node(values.pop(0))
    leaves = set()

    for value in values:
        node = root
        depth = 0
        inserted = False

        while depth < height and not inserted:
            attr = 'left' if node.value > value else 'right'
            if getattr(node, attr) is None:
                setattr(node, attr, Node(value))
                inserted = True
            node = getattr(node, attr)
            depth += 1

        if inserted and depth == height:
            leaves.add(node)
        if len(leaves) == leaf_count:
            break

    return root


def heap(height=3, is_max=True, is_perfect=False):
    """Generate a heap and return its root node.

    :param height: The height of the heap (default: 3, range: 0 - 9 inclusive).
    :type height: int
    :param is_max: If set to True (default: True), generate a max heap.
        Otherwise, generate a min heap. Note that a binary tree with only the
        root is both a min and max heap.
    :type is_max: bool
    :param is_perfect: If set to True (default: False), a perfect heap with all
        levels filled is returned. When set to False, a perfect heap may still
        be generated and returned by chance.
    :type is_perfect: bool
    :return: The root node of the generated heap.
    :rtype: binarytree.Node
    :raise binarytree.exceptions.InvalidTreeHeightError:
        If an invalid tree height is given.

    **Example**:

    .. doctest::

        >>> from binarytree import heap
        >>>
        >>> root = heap()
        >>>
        >>> root.height
        3
        >>> root.is_max_heap
        True

    .. doctest::

        >>> from binarytree import heap
        >>>
        >>> root = heap(4, is_max=False)
        >>>
        >>> root.height
        4
        >>> root.is_min_heap
        True

    .. doctest::

        >>> from binarytree import heap
        >>>
        >>> root = heap(5, is_max=False, is_perfect=True)
        >>>
        >>> root.height
        5
        >>> root.is_min_heap
        True
        >>> root.is_perfect
        True

    .. doctest::

        >>> from binarytree import heap
        >>>
        >>> root = heap(-1)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
         ...
        InvalidTreeHeightError: The height must be an integer between 0 - 9
    """
    _validate_tree_height(height)
    values = _generate_random_node_values(height)

    if not is_perfect:
        # Randomly cut some of the leaf nodes away
        random_cut = random.randint(2 ** height, len(values))
        values = values[:random_cut]

    if is_max:
        negated = [-v for v in values]
        heapq.heapify(negated)
        return build([-v for v in negated])
    else:
        heapq.heapify(values)
        return build(values)
