__all__ = ['Node']

import numbers
from binarytree.exceptions import (
    NodeValueError,
    NodeIndexError,
    NodeTypeError,
    NodeModifyError,
    NodeNotFoundError,
    NodeReferenceError,
)


def _is_balanced(root):
    """Return the height if the binary tree is balanced, -1 otherwise."""
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
    """Check if the binary tree is a BST (binary search tree)."""
    if root is None:
        return True
    return (
        min_value < root.value < max_value and
        _is_bst(root.left, min_value, root.value) and
        _is_bst(root.right, root.value, max_value)
    )


def _build_tree_string(root, curr_index, index=False, delimiter='-'):
    """Recursively walk down the binary tree and build a pretty-print string.

    In each recursive call, a "box" of characters visually representing the
    current (sub)tree is constructed line by line. Each line is padded with
    whitespaces to ensure all lines in the box have the same length. Then the
    box, its width, and start-end positions of its root node value repr string
    (required for drawing branches) are sent up to the parent call. The parent
    call then combines its left and right sub-boxes to build a larger box etc."""
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

    # Draw the branch connecting the current root node to the left sub-box
    # Pad the line with whitespaces where necessary
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

    # Draw the representation of the current root node
    line1.append(node_repr)
    line2.append(' ' * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box
    # Pad the line with whitespaces where necessary
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

    # Return the new box, its width and its root repr positions
    return new_box, len(new_box[0]), new_root_start, new_root_end


def _get_tree_properties(root):
    """Inspect the binary tree and return its properties (e.g. height)."""
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

            # Node is a leaf.
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

    This class provides methods and properties for managing the current node
    instance, and the binary tree in which the node is the root of. When a
    docstring in this class mentions "binary tree", it is referring to the
    current node and its descendants."""

    def __init__(self, value, left=None, right=None):
        if not isinstance(value, numbers.Number):
            raise NodeValueError('node value must be a number')
        if left is not None and not isinstance(left, Node):
            raise NodeTypeError('left child must be a Node instance')
        if right is not None and not isinstance(right, Node):
            raise NodeTypeError('right child must be a Node instance')

        self.value = value
        self.left = left
        self.right = right

    def find_node(self, value):
        if value == self.value:
            return self
        elif value < self.value and self.left is not None:
            return self.left.find_node(value)
        elif value > self.value and self.right is not None:
            return self.right.find_node(value)
        else:
            return None

    def insert_node(self, value, first_run=True):
        if first_run and self.find_node(value) is not None:
            return

        elif self.value == None:
            self.value = value

        elif value < self.value:
            if self.left is None:
                self.left = Node(value)
            else:
                self.left.insert_node(value, False)

        elif value > self.value:
            if self.right is None:
                self.right = Node(value)
            else:
                self.right.insert_node(value, False)

    def remove_node(self, value, first_run=True):
        if first_run and self.find_node(value) is None:
            return

        elif value == self.value:
            self.left = None
            self.right = None
            self.value = None

        elif value < self.value:
            if self.left is not None and value == self.left.value:
                self.left = None
            else:
                self.left.remove_node(value, False)

        elif value > self.value:
            if self.right is not None and value == self.right.value:
                self.right = None
            else:
                self.right.remove_node(value, False)

    def __repr__(self):
        """Return the string representation of the current node."""
        return 'Node({})'.format(self.value)

    def __str__(self):
        """Return the pretty-print string for the binary tree."""
        lines = _build_tree_string(self, 0, False, '-')[0]
        return '\n' + '\n'.join((line.rstrip() for line in lines))

    def __setattr__(self, attr, obj):
        """Modified version of ``__setattr__`` with extra sanity checking."""
        if attr == 'left':
            if obj is not None and not isinstance(obj, Node):
                raise NodeTypeError(
                    'left child must be a Node instance')
        elif attr == 'right':
            if obj is not None and not isinstance(obj, Node):
                raise NodeTypeError(
                    'right child must be a Node instance')
        elif attr == 'value':
            if obj is not None and not isinstance(obj, numbers.Number):
                raise NodeValueError('node value must be a number')

        object.__setattr__(self, attr, obj)

    def __iter__(self):
        """Iterate through the nodes in the binary tree in level-order_."""
        current_nodes = [self]

        while len(current_nodes) > 0:
            next_nodes = []
            for node in current_nodes:
                yield node
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            current_nodes = next_nodes

    def __len__(self):
        """Return the total number of nodes in the binary tree."""
        return self.properties['size']

    def __getitem__(self, index):
        """Return the node (or subtree) at the given level-order_ index."""
        if not isinstance(index, int) or index < 0:
            raise NodeIndexError(
                'node index must be a non-negative int')

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

        raise NodeNotFoundError('node missing at index {}'.format(index))

    def __setitem__(self, index, node):
        """Insert a node (or subtree) at the given level-order_ index."""
        if index == 0:
            raise NodeModifyError('cannot modify the root node')

        parent_index = (index - 1) // 2
        try:
            parent = self.__getitem__(parent_index)
        except NodeNotFoundError:
            raise NodeNotFoundError(
                'parent node missing at index {}'.format(parent_index))

        setattr(parent, 'left' if index % 2 else 'right', node)

    def __delitem__(self, index):
        """Remove the node (or subtree) at the given level-order_ index."""
        if index == 0:
            raise NodeModifyError('cannot delete the root node')

        parent_index = (index - 1) // 2
        try:
            parent = self.__getitem__(parent_index)
        except NodeNotFoundError:
            raise NodeNotFoundError(
                'no node to delete at index {}'.format(index))

        child_attr = 'left' if index % 2 == 1 else 'right'
        if getattr(parent, child_attr) is None:
            raise NodeNotFoundError(
                'no node to delete at index {}'.format(index))

        setattr(parent, child_attr, None)

    def pprint(self, index=False, delimiter='-'):
        """Pretty-print the binary tree."""
        lines = _build_tree_string(self, 0, index, delimiter)[0]
        print('\n' + '\n'.join((line.rstrip() for line in lines)))

    def validate(self):
        """Check if the binary tree is malformed."""
        has_more_nodes = True
        visited = set()
        to_visit = [self]
        index = 0

        while has_more_nodes:
            has_more_nodes = False
            next_nodes = []

            for node in to_visit:
                if node is None:
                    next_nodes.extend((None, None))
                else:
                    if node in visited:
                        raise NodeReferenceError(
                            'cyclic node reference at index {}'.format(index))
                    if not isinstance(node, Node):
                        raise NodeTypeError(
                            'invalid node instance at index {}'.format(index))
                    if not isinstance(node.value, numbers.Number):
                        raise NodeValueError(
                            'invalid node value at index {}'.format(index))
                    if node.left is not None or node.right is not None:
                        has_more_nodes = True
                    visited.add(node)
                    next_nodes.extend((node.left, node.right))
                index += 1

            to_visit = next_nodes

    @property
    def values(self):
        """Return the `list representation`_ of the binary tree."""
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

        # Get rid of trailing None's
        while values and values[-1] is None:
            values.pop()

        return values

    @property
    def leaves(self):
        """Return the leaf nodes of the binary tree."""
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
        """Return the nodes in the binary tree level by level."""
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
        """Return the height of the binary tree."""
        return _get_tree_properties(self)['height']

    @property
    def size(self):
        """Return the total number of nodes in the binary tree."""
        return _get_tree_properties(self)['size']

    @property
    def leaf_count(self):
        """Return the total number of leaf nodes in the binary tree."""
        return _get_tree_properties(self)['leaf_count']

    @property
    def is_balanced(self):
        """Check if the binary tree is height-balanced."""
        return _is_balanced(self) >= 0

    @property
    def is_bst(self):
        """Check if the binary tree is a BST_ (binary search tree)."""
        return _is_bst(self, float('-inf'), float('inf'))

    @property
    def is_max_heap(self):
        """Check if the binary tree is a `max heap`_."""
        return _get_tree_properties(self)['is_max_heap']

    @property
    def is_min_heap(self):
        """Check if the binary tree is a `min heap`_."""
        return _get_tree_properties(self)['is_min_heap']

    @property
    def is_perfect(self):
        """Check if the binary tree is perfect."""
        return _get_tree_properties(self)['is_perfect']

    @property
    def is_strict(self):
        """Check if the binary tree is strict."""
        return _get_tree_properties(self)['is_strict']

    @property
    def is_complete(self):
        """Check if the binary tree is complete."""
        return _get_tree_properties(self)['is_complete']

    @property
    def min_node_value(self):
        """Return the minimum node value of the binary tree."""
        return _get_tree_properties(self)['min_node_value']

    @property
    def max_node_value(self):
        """Return the maximum node value of the binary tree."""
        return _get_tree_properties(self)['max_node_value']

    @property
    def max_leaf_depth(self):
        """Return the maximum leaf node depth of the binary tree."""
        return _get_tree_properties(self)['max_leaf_depth']

    @property
    def min_leaf_depth(self):
        """Return the minimum leaf node depth of the binary tree."""
        return _get_tree_properties(self)['min_leaf_depth']

    @property
    def properties(self):
        """Return various properties of the binary tree."""
        properties = _get_tree_properties(self)
        properties.update({
            'is_bst': _is_bst(self),
            'is_balanced': _is_balanced(self) >= 0
        })
        return properties

    @property
    def inorder(self):
        """Return the nodes in the binary tree using in-order_ traversal."""
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
        """Return the nodes in the binary tree using pre-order_ traversal."""
        node_stack = [self]
        result = []

        while len(node_stack) > 0:
            node = node_stack.pop()
            result.append(node)

            if node.right is not None:
                node_stack.append(node.right)
            if node.left is not None:
                node_stack.append(node.left)

        return result

    @property
    def postorder(self):
        """Return the nodes in the binary tree using post-order_ traversal."""
        node_stack = []
        result = []
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
                result.append(node)
                node = None

            if len(node_stack) == 0:
                break

        return result

    @property
    def levelorder(self):
        """Return the nodes in the binary tree using level-order_ traversal."""
        current_nodes = [self]
        result = []

        while len(current_nodes) > 0:
            next_nodes = []
            for node in current_nodes:
                result.append(node)
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            current_nodes = next_nodes

        return result

r = Node(4)
r.insert_node(2)
r.insert_node(1)
r.insert_node(3)
r.insert_node(5)
print(r.inorder)
print(r.preorder)
print(r.postorder)
print(r.levelorder)
print(list(r))
