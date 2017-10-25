from inspect import isclass
from heapq import heapify
from random import sample, random


def no_op(value):  # pragma: no cover
    return value


_node_init = no_op
_node_cls = None
_null = None
_left_attr = 'left'
_right_attr = 'right'
_parent_attr = 'parent'
_value_attr = 'value'
_id_attr = 'level_order_id'


class Node(object):
    """Represents a binary tree node."""

    def __init__(self, value, parent=_null):
        self.__setattr__(_value_attr, value)
        self.__setattr__(_left_attr, _null)
        self.__setattr__(_right_attr, _null)
        if parent is not _null and isinstance(parent, Node):
            self.__setattr__(_parent_attr, parent)
        else:
            self.__setattr__(_parent_attr, _null)

    def __repr__(self):
        return 'Node({})'.format(
            self.__getattribute__(_value_attr)
        )

    def __setattr__(self, name, value):
        # Magically set the parent to self when a child is created
        if (name in [_left_attr, _right_attr]
                and value is not _null
                and isinstance(value, Node)):
            value.parent = self
        object.__setattr__(self, name, value)

    def convert(self):
        return convert(self)

    def inspect(self):
        return inspect(self)

    def subtree(self, node_id):
        return subtree(self, node_id)

    def prune(self, node_id):
        return prune(self, node_id)

    def is_root(self):
        return self.parent is _null

    def is_leaf(self):
        return self.right is _null and self.left is _null

    def leafs(self, values_only=False):
        return leafs(self, values_only)

    def level(self):
        return 0 if self.parent == _null else self.parent.level() + 1

    def show(self):
        show(self)

    def show_ids(self):
        show_ids(self)

    def show_all(self):
        show_all(self)


def _create_node(value, parent=_null):
    """Create and return a new node."""
    if _node_init != no_op:
        return _node_init(value)
    return (_node_cls or Node)(value, parent=parent)


def _is_list(obj):
    """Return ``True`` if the object is a list, else ``False``."""
    return isinstance(obj, list)


def _is_node(obj):
    """Return ``True`` if the object is a node, else ``False``."""
    return isinstance(obj, _node_cls or Node)


def _id_of(node):
    """Return the level-order ID of the node."""
    return getattr(node, _id_attr)


def _value_of(node):
    """Return the value of the node."""
    return getattr(node, _value_attr)


def _parent_of(node):
    """Return the parent of the node."""
    return getattr(node, _parent_attr)


def _left_of(node):
    """Return the left child of the node."""
    return getattr(node, _left_attr)


def _right_of(node):
    """Return the right child of the node."""
    return getattr(node, _right_attr)


def _set_left(node, child):
    """Set the child to the left of the node."""
    setattr(node, _left_attr, child)


def _set_right(node, child):
    """Set the child to the right of the node."""
    setattr(node, _right_attr, child)


def _set_id(node, node_id):
    """Set the level-order ID of the node."""
    setattr(node, _id_attr, node_id)


def _copy_with_id(node, node_id):
    """Return a copy of the node with the level-order ID injected."""
    node_copy = _create_node(_value_of(node), parent=_parent_of(node))
    _set_id(node_copy, node_id)
    return node_copy


def _prune_left(node):
    """Prune the left subtree of the node."""
    node.__setattr__(_left_attr, _null)


def _prune_right(node):
    """Prune the right subtree of the node."""
    node.__setattr__(_right_attr, _null)


def _is_balanced(node):
    """Return the depth if balanced else -1."""
    if node == _null:
        return 0

    left = _is_balanced(_left_of(node))
    if left < 0:
        return -1

    right = _is_balanced(_right_of(node))
    if right < 0 or abs(left - right) > 1:
        return -1

    return max(left, right) + 1


def _is_bst(node, min_val=float('-inf'), max_val=float('inf')):
    """Return True if and only if the tree is a binary search tree."""
    if node == _null:
        return True

    if (min_val != _null and _value_of(node) <= min_val):
        return False

    if (max_val != _null and _value_of(node) >= max_val):
        return False

    return _is_bst(_left_of(node), min_val, _value_of(node)) and \
           _is_bst(_right_of(node), _value_of(node), max_val)


def _build_list(root):
    """Build a list from a tree and return it."""
    result = []
    current_nodes = [root]
    level_not_empty = True

    while level_not_empty:
        level_not_empty = False
        next_nodes = []

        for node in current_nodes:
            if node == _null:
                result.append(_null)
                next_nodes.append(_null)
                next_nodes.append(_null)
            else:
                result.append(_value_of(node))

                left_child = _left_of(node)
                right_child = _right_of(node)

                if left_child != _null:
                    level_not_empty = True
                if right_child != _null:
                    level_not_empty = True

                next_nodes.append(left_child)
                next_nodes.append(right_child)

        current_nodes = next_nodes

    while result and result[-1] == _null:
        result.pop()
    return result


def _build_tree(values):
    """Build a tree from a list and return its root."""
    if not values:
        return _null

    nodes = [_null for _ in values]
    if values[0] == _null:
        raise ValueError('Node missing at index 0')

    root = _create_node(values[0], parent=_null)
    nodes[0] = root

    index = 1
    while index < len(values):
        value = values[index]
        if value != _null:
            parent_index = int((index + 1) / 2) - 1
            parent_node = nodes[parent_index]
            if parent_node == _null:
                raise ValueError(
                    'Node missing at index {}'
                    .format(parent_index)
                )
            child_node = _create_node(value, parent=parent_node)
            if index % 2:  # is odd
                _set_left(parent_node, child_node)
            else:
                _set_right(parent_node, child_node)
            nodes[index] = child_node
        index += 1

    return root


def _build_repr(node, with_ids=False, with_values=True):
    """Recursive function used for pretty-printing the binary tree.

    In each recursive call, a "box" of characters visually representing the
    current subtree is constructed line by line. Each line is padded with
    whitespaces to ensure all lines have the same length. The box, its width,
    and the start-end positions of its root (used for drawing branches) are
    sent up to the parent call, which then combines left and right sub-boxes
    to build a bigger box etc.
    """
    if node == _null:
        return [], 0, 0, 0

    if with_ids and with_values:
        node_repr = "{}:{}".format(_id_of(node), _value_of(node))
    elif with_ids and not with_values:
        node_repr = str(_id_of(node))
    elif not with_ids and with_values:
        node_repr = str(_value_of(node))
    else:  # pragma: no cover
        node_repr = "O"

    line1 = []
    line2 = []
    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths and their root positions
    l_box, l_box_width, l_root_start, l_root_end = \
        _build_repr(_left_of(node), with_ids, with_values)
    r_box, r_box_width, r_root_start, r_root_end = \
        _build_repr(_right_of(node), with_ids, with_values)

    # Draw the branch connecting the new root to the left sub-box,
    # padding with whitespaces where necessary
    if l_box_width > 0:
        l_root = -int(-(l_root_start + l_root_end) / 2) + 1  # ceiling
        line1.append(' ' * (l_root + 1))
        line1.append('_' * (l_box_width - l_root))
        line2.append(' ' * l_root + '/')
        line2.append(' ' * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the new root
    line1.append(node_repr)
    line2.append(' ' * new_root_width)

    # Draw the branch connecting the new root to the right sub-box,
    # padding with whitespaces where necessary
    if r_box_width > 0:
        r_root = int((r_root_start + r_root_end) / 2)  # floor
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


def _bst_insert(root, value):
    """Insert a node into the BST."""
    depth = 1
    node = root
    while True:
        if _value_of(node) > value:
            left_child = _left_of(node)
            if left_child == _null:
                _set_left(node, _create_node(value, parent=node))
                break
            node = left_child
        else:
            right_child = _right_of(node)
            if right_child == _null:
                _set_right(node, _create_node(value, parent=node))
                break
            node = right_child
        depth += 1
    return depth


def _random_insert(root, value):
    """Insert a node randomly into the binary tree."""
    depth = 1
    node = root
    while True:
        if random() < 0.5:
            left_child = _left_of(node)
            if left_child == _null:
                _set_left(node, _create_node(value, parent=node))
                break
            node = left_child
        else:
            right_child = _right_of(node)
            if right_child == _null:
                _set_right(node, _create_node(value, parent=node))
                break
            node = right_child
        depth += 1
    return depth


def _inject_ids(root):
    """Return a new copy of the tree with node IDs injected."""
    root_copy = _copy_with_id(root, 0)
    id_counter = 1

    current_nodes = [root]
    current_copies = [root_copy]

    while current_nodes:
        next_nodes = []
        next_copies = []

        index = 0
        while index < len(current_nodes):
            node = current_nodes[index]
            node_copy = current_copies[index]

            left_child = _left_of(node)
            right_child = _right_of(node)

            if left_child != _null:
                next_nodes.append(left_child)
                left_child_copy = _copy_with_id(left_child, id_counter)
                _set_left(node_copy, left_child_copy)
                next_copies.append(left_child_copy)
                id_counter += 1

            if right_child != _null:
                next_nodes.append(right_child)
                right_child_copy = _copy_with_id(right_child, id_counter)
                _set_right(node_copy, right_child_copy)
                next_copies.append(right_child_copy)
                id_counter += 1
            index += 1

        current_nodes = next_nodes
        current_copies = next_copies

    return root_copy


def _validate_tree(root):
    """Check if the tree is malformed."""
    current_nodes = [root]

    while current_nodes:
        next_nodes = []
        for node in current_nodes:
            if _is_node(node):
                if _value_of(node) == _null:
                    raise ValueError('A node cannot have a null value')
                next_nodes.append(_left_of(node))
                next_nodes.append(_right_of(node))
            elif node != _null:
                # Halt if the node is not NULL nor a node instance
                raise ValueError('Found an invalid node in the tree')
        current_nodes = next_nodes

    return root


def _prepare_tree(bt):
    """Prepare the binary tree for tree algorithms."""
    if _is_list(bt):
        return _build_tree(bt)
    if _is_node(bt):
        return _validate_tree(bt)
    raise ValueError('Expecting a list or a node')


def _validate_id(node_id):
    """Check if the ID is valid."""
    if not isinstance(node_id, int):
        raise ValueError('The node ID must be an integer')
    if node_id < 0:
        raise ValueError('The node ID must start from 0')


def _generate_values(height, multiplier=1):
    """Generate and return a list of random node values."""
    if not isinstance(height, int) or height < 0:
        raise ValueError('Height must be a non-negative integer')
    count = 2 ** (height + 1) - 1
    return sample(range(count * multiplier), count)


def customize(node_class,
              node_init,
              null_value,
              value_attr,
              left_attr,
              right_attr):
    """Set up a custom specification for the binary tree node.

    :param node_class: The binary tree node class.
    :type node_class: type
    :param node_init: The node initializer function which must take the
        node value as the only argument and return an instance of node_class.
    :type node_init: callable
    :param null_value: The null/sentinel value.
    :type null_value: object
    :param value_attr: The attribute name reserved for the node value.
    :type value_attr: str | unicode
    :param left_attr: The attribute name reserved for the left child.
    :type left_attr: str | unicode
    :param right_attr: The attribute name reserved for the right child.
    :type right_attr: str | unicode
    :raises ValueError: If an invalid set of arguments is given.
    """
    global _node_cls
    global _node_init
    global _null
    global _value_attr
    global _left_attr
    global _right_attr

    # Do some sanity checking on the arguments
    if not isclass(node_class):
        raise ValueError('Invalid class given for the node')
    try:
        node = node_init(2 if null_value == 1 else 1)
    except:
        raise ValueError(
            'The node initializer function must be a callable which '
            'takes the node value as its only argument'
        )
    if not isinstance(node, node_class):
        raise ValueError(
            'The node initializer function must be a callable which '
            'returns an instance of "{}"'.format(node_class.__name__)
        )
    for attribute in [value_attr, left_attr, right_attr]:
        if not hasattr(node, attribute):
            raise ValueError(
                'The node class does not have one of the required '
                'attributes "{}"'.format(attribute)
            )
    if getattr(node, left_attr) != null_value:
        raise ValueError(
            'The node class does not initialize instances with expected '
            'null/sentinel value "{}" for its left child node attribute '
            '"{}"'.format(null_value, left_attr)
        )
    if getattr(node, right_attr) != null_value:
        raise ValueError(
            'The node class does not initialize instances with expected '
            'null/sentinel value "{}" for its right child node attribute '
            '"{}"'.format(null_value, right_attr)
        )

    _node_cls = node_class
    _node_init = node_init
    _null = null_value
    _value_attr = value_attr
    _left_attr = left_attr
    _right_attr = right_attr


def tree(height=4, is_balanced=False):
    """Generate a random binary tree and return its root.

    :param height: The height of the tree (default: 4).
    :type height: int
    :param is_balanced: The tree is weight-balanced (default: ``False``).
    :type is_balanced: bool
    :return: The root of the generated binary tree.
    :rtype: binarytree.Node
    :raises ValueError: If an invalid binary tree is given.
    """
    values = _generate_values(height)
    if is_balanced:
        return _build_tree(values)

    root = _create_node(values[0])
    for index in range(1, len(values)):
        depth = _random_insert(root, values[index])
        if depth == height:
            break
    return root


def bst(height=4):
    """Generate a random binary search tree and return its root.

    :param height: The height of the tree (default: 4).
    :type height: int
    :return: The root node of the generated binary search tree.
    :rtype: binarytree.Node
    :raises ValueError: If an invalid binary tree is given.
    """
    values = _generate_values(height)
    root = _create_node(values[0])
    for index in range(1, len(values)):
        depth = _bst_insert(root, values[index])
        if depth == height:
            break
    return root


def heap(height=4, is_max=False):
    """Generate a random min/max heap and return its root.

    :param height: The height of the tree (default: 4).
    :type height: int
    :param is_max: Whether to generate a max or min heap.
    :type is_max: bool
    :return: The root node of the generated heap.
    :rtype: binarytree.Node
    :raises ValueError: If an invalid binary tree is given.
    """
    values = _generate_values(height)
    if is_max:
        negated = [-v for v in values]
        heapify(negated)
        return _build_tree([-v for v in negated])
    else:
        heapify(values)
        return _build_tree(values)


def stringify(bt, with_ids=False, with_values=True):
    """Return the string representation of the binary tree.

    :param bt: The binary tree.
    :type bt: list | binarytree.Node
    :param with_ids: Add level-order IDs into the nodes.
    :type with_ids: bool
    :param with_values: Display node values.
    :type with_values: bool
    :return: The string representation.
    :rtype: str | unicode
    :raises ValueError: If an invalid binary tree is given.
    """
    if bt == _null:
        return ''
    if _is_list(bt) and not bt:
        return ''

    bt = _prepare_tree(bt)
    if with_ids:
        bt = _inject_ids(bt)
    return '\n' + '\n'.join(_build_repr(bt, with_ids, with_values)[0])


def show(bt):
    """Pretty print the binary tree (the node values).

    :param bt: The binary tree to pretty-print.
    :type bt: list | binarytree.Node
    :return: None
    :rtype: None
    :raises ValueError: If an invalid binary tree is given.
    """
    print(stringify(bt, with_ids=False, with_values=True))


def show_all(bt):
    """Pretty print the binary tree with both the level-order IDs and values.

    :param bt: The binary tree to pretty-print.
    :type bt: list | binarytree.Node
    :return: None
    :rtype: None
    :raises ValueError: If an invalid binary tree is given.
    """
    print(stringify(bt, with_ids=True, with_values=True))


def show_ids(bt):
    """Pretty print the binary tree showing just the level-order node IDs.

    :param bt: The binary tree to pretty-print.
    :type bt: list | binarytree.Node
    :return: None
    :rtype: None
    :raises ValueError: If an invalid binary tree is given.
    """
    print(stringify(bt, with_ids=True, with_values=False))


def pprint(bt):
    """Pretty print the binary tree.

    Equivalent to `show`. Still here for backwards compatibility.

    :param bt: The binary tree to pretty-print.
    :type bt: list | binarytree.Node
    :return: None
    :rtype: None
    :raises ValueError: If an invalid binary tree is given.
    """
    show(bt)


def convert(bt):
    """Convert a binary tree into a list, or vice versa.

    :param bt: The binary tree to convert.
    :type bt: list | binarytree.Node
    :return: The converted form of the binary tree.
    :rtype: list | binarytree.Node
    :raises ValueError: If an invalid binary tree is given.
    """
    if bt == _null:
        return []
    if _is_list(bt):
        return _build_tree(bt)
    if _is_node(bt):
        return _build_list(_validate_tree(bt))
    raise ValueError('Expecting a list or a node')


def get_level(bt, level, show_values=False, show_nulls=False):
    """Return the requested level of the binary tree, ordered from left to right.

    If a node other than the root node is passed in, then this function
    returns the requested level of the tree relative to the passed in node.

    :param bt: The binary tree.
    :type bt: binarytree.Node
    :param level: The requested level to return.
    :type level: int
    :param show_values: whether to convert nodes to values before returning.
    :type show_values: boolean
    :param show_nulls: whether to show where empty nodes are.
    :type show_nulls: boolean
    :return: dictionary of form {0:[rootnode], 1:[1st, level, nodes]}
    :rtype: dictionary
    """
    bt = _prepare_tree(bt)
    if not isinstance(level, int) or level < 0:
        raise ValueError("Requested level must be a non-negative integer.")
    current_nodes = [bt]
    current_level = 0

    while current_level < level:
        next_nodes = []
        index = 0

        while index < len(current_nodes):
            node = current_nodes[index]
            left_child = _left_of(node)
            right_child = _right_of(node)

            if left_child != _null:
                next_nodes.append(left_child)
            elif show_nulls is True:
                next_nodes.append(Node(_null))
            if right_child != _null:
                next_nodes.append(right_child)
            elif show_nulls is True:
                next_nodes.append(Node(_null))
            index += 1

        if len(next_nodes) == 0 or all(node.value is _null for node in next_nodes):
            raise ValueError("Requested level not present in tree.")
        current_nodes = next_nodes
        current_level += 1

    return [node.value for node in current_nodes] if show_values else current_nodes


def get_levels(bt, show_values=False, show_nulls=False):
    """Return the levels of the binary tree, ordered from left to right.

    If a node other than the root node is passed in, then this function
    returns the levels of the tree relative to the passed in node.

    :param bt: The binary tree.
    :type bt: binarytree.Node
    :param show_values: whether to convert nodes to values before returning.
    :type show_values: boolean
    :param show_nulls: whether to show where empty nodes are.
    :type show_nulls: boolean
    :return: dictionary of form {0:[rootnode], 1:[1st, level, nodes]}
    :rtype: dictionary
    """
    bt = _prepare_tree(bt)

    current_nodes = [bt]
    levels = []
    current_level = 0

    while len(current_nodes) != 0 and not all(node.value is _null for node in current_nodes):
        levels.append(current_nodes)
        next_nodes = []
        index = 0

        while index < len(current_nodes):
            node = current_nodes[index]
            left_child = _left_of(node)
            right_child = _right_of(node)

            if left_child != _null:
                next_nodes.append(left_child)
            elif show_nulls is True:
                next_nodes.append(_create_node(_null))
            if right_child != _null:
                next_nodes.append(right_child)
            elif show_nulls is True:
                next_nodes.append(_create_node(_null))
            index += 1

        current_nodes = next_nodes
        current_level += 1

    if show_values is True:
        for level in range(len(levels)):
            levels[level] = [node.value for node in levels[level]]
    return levels


def inspect(bt):
    """Return the properties of the binary tree.

    :param bt: The binary tree to inspect.
    :type bt: list | binarytree.Node
    :return: The various properties of the binary tree.
    :rtype: dict
    :raises ValueError: If an invalid binary tree is given.
    """
    bt = _prepare_tree(bt)

    is_full = True
    is_descending = True
    is_ascending = True
    is_left_padded = True
    min_value = float('inf')
    max_value = float('-inf')
    node_count = 0
    leaf_count = 0
    min_leaf_depth = 0
    current_depth = -1
    current_nodes = [bt]

    while current_nodes:

        null_encountered = False
        current_depth += 1
        next_nodes = []

        for node in current_nodes:
            num_of_children = 0
            node_count += 1
            node_value = _value_of(node)
            min_value = min(node_value, min_value)
            max_value = max(node_value, max_value)

            left_child = _left_of(node)
            right_child = _right_of(node)

            for child in (left_child, right_child):
                if child != _null and null_encountered:
                    is_left_padded = False
                elif child == _null and not null_encountered:
                    null_encountered = True

            if left_child == _null and right_child == _null:
                if min_leaf_depth == 0:
                    min_leaf_depth = current_depth
                leaf_count += 1

            if left_child != _null:
                if _value_of(left_child) > node_value:
                    is_descending = False
                elif _value_of(left_child) < node_value:
                    is_ascending = False
                next_nodes.append(left_child)
                num_of_children += 1

            if right_child != _null:
                if _value_of(right_child) > node_value:
                    is_descending = False
                elif _value_of(right_child) < node_value:
                    is_ascending = False
                next_nodes.append(right_child)
                num_of_children += 1
            if num_of_children == 1:
                is_full = False

        current_nodes = next_nodes

    is_balanced = _is_balanced(bt) >= 0

    return {
        'is_height_balanced': current_depth - min_leaf_depth < 2,
        'is_weight_balanced': is_balanced,
        'is_max_heap': is_descending and is_left_padded and is_balanced,
        'is_min_heap': is_ascending and is_left_padded and is_balanced,
        'is_bst': _is_bst(bt),
        'height': current_depth,
        'leaf_count': leaf_count,
        'node_count': node_count,
        'min_leaf_depth': min_leaf_depth,
        'max_leaf_depth': current_depth,
        'min_value': min_value,
        'max_value': max_value,
        'is_full': is_full
    }


def subtree(bt, node_id):
    """Return the node and its children (i.e. subtree) of the level-order ID.

    If the binary tree is given as a list, it is automatically converted
    into a tree form first.

    :param bt: The binary tree.
    :type bt: list | binarytree.Node
    :param node_id: The level-order ID of the node.
    :type node_id: int
    :return: The root of the subtree.
    :rtype: binarytree.Node
    :raises ValueError: If an invalid binary tree or node ID is given.
    """
    bt = _prepare_tree(bt)
    _validate_id(node_id)

    current_nodes = [bt]
    current_id = 0

    while current_nodes:
        next_nodes = []

        for node in current_nodes:
            if current_id == node_id:
                return node
            current_id += 1

            left_child = _left_of(node)
            right_child = _right_of(node)

            if left_child != _null:
                next_nodes.append(left_child)
            if right_child != _null:
                next_nodes.append(right_child)

        current_nodes = next_nodes

    raise ValueError('Cannot find node with ID {}'.format(node_id))


def prune(bt, node_id):
    """Delete the node and all of its children from the binary tree.

    If the binary tree is given as a list, it is automatically converted
    into a tree form first.

    :param bt: The binary tree.
    :type bt: list | binarytree.Node
    :param node_id: The level-order ID of the node.
    :type node_id: int
    :return: The root node of the binary tree with the node pruned.
    :rtype: binarytree.Node
    :raises ValueError: If an invalid binary tree or node ID is given.
    """
    bt = _prepare_tree(bt)
    if node_id == 0:
        raise ValueError('Cannot prune the root node')
    _validate_id(node_id)

    current_parents = {}
    current_nodes = [bt]
    current_id = 0

    while current_nodes:
        next_nodes = []
        next_parents = {}

        for node in current_nodes:
            if current_id == node_id:
                parent = current_parents[node]
                if _left_of(parent) == node:
                    _prune_left(parent)
                else:
                    _prune_right(parent)
                return bt

            left_child = _left_of(node)
            right_child = _right_of(node)

            if left_child != _null:
                next_nodes.append(left_child)
                next_parents[left_child] = node
            if right_child != _null:
                next_nodes.append(right_child)
                next_parents[right_child] = node
            current_id += 1

        current_nodes = next_nodes
        current_parents = next_parents

    raise ValueError('Cannot find node with ID {}'.format(node_id))


def leafs(bt, values_only=False):
    """Return the leaf nodes of the binary tree.

    If the binary tree is given as a list, it is automatically converted
    into a tree form first.

    :param bt: The binary tree.
    :type bt: list | binarytree.Node
    :param values_only: Return the node values only rather than the nodes.
    :type values_only: bool
    :return: The list of leaf nodes.
    :rtype: [binarytree.Node] | [int]
    :raises ValueError: If an invalid binary tree is given.
    """
    bt = _prepare_tree(bt)

    current_nodes = [bt]
    leaf_nodes = []

    while current_nodes:
        next_nodes = []

        for node in current_nodes:
            left_child = _left_of(node)
            right_child = _right_of(node)

            if left_child == _null and right_child == _null:
                leaf_nodes.append(node)
            if left_child != _null:
                next_nodes.append(left_child)
            if right_child != _null:
                next_nodes.append(right_child)

        current_nodes = next_nodes

    return [_value_of(n) for n in leaf_nodes] if values_only else leaf_nodes
