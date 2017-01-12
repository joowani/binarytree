import inspect as inspect_
from heapq import heapify
from random import sample, random

_node_init_func = None
_node_cls = None
_null = None
_left_attr = 'left'
_right_attr = 'right'
_value_attr = 'value'


class Node(object):
    """Represents a binary tree node."""

    def __init__(self, value):
        self.__setattr__(_value_attr, value)
        self.__setattr__(_left_attr, _null)
        self.__setattr__(_right_attr, _null)

    def __repr__(self):
        return 'Node({})'.format(
            self.__getattribute__(_value_attr)
        )

    def __str__(self):
        return stringify(self)

    def to_list(self):
        return convert(self)

    def inspect(self):
        return inspect(self)


def _new_node(value):
    """Create and return a new node."""
    if _node_init_func is not None:
        return _node_init_func(value)
    return (_node_cls or Node)(value)


def _is_list(obj):
    """Return True if the object is a list, else False."""
    return isinstance(obj, list)


def _is_node(obj):
    """Return True if the object is a node, else False."""
    return isinstance(obj, _node_cls or Node)


def _value_of(node):
    """Return the value of the node."""
    return getattr(node, _value_attr)


def _left_of(node):
    """Return the left child of the node."""
    return getattr(node, _left_attr)


def _right_of(node):
    """Return the right child of the node."""
    return getattr(node, _right_attr)


def _add_left(parent, child):
    """Add the child to the left of the parent."""
    setattr(parent, _left_attr, child)


def _add_right(parent, child):
    """Add the child to the right of the parent."""
    setattr(parent, _right_attr, child)


def _is_balanced(node):
    """Return depth if balanced else -1."""
    if node == _null:
        return 0

    left = _is_balanced(_left_of(node))
    right = _is_balanced(_right_of(node))

    if left < 0 or right < 0 or abs(left - right) > 1:
        return -1
    return max(left, right) + 1


def _build_list(root):
    """Build a list from a tree and return it"""
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

    root = _new_node(values[0])
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
            child_node = _new_node(value)
            if index % 2:  # is odd
                _add_left(parent_node, child_node)
            else:
                _add_right(parent_node, child_node)
            nodes[index] = child_node
        index += 1

    return root


def _build_str(node):
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

    line1 = []
    line2 = []
    new_root_width = gap_size = len(str(_value_of(node)))

    # Get the left and right sub-boxes, their widths and their root positions
    l_box, l_box_width, l_root_start, l_root_end = _build_str(_left_of(node))
    r_box, r_box_width, r_root_start, r_root_end = _build_str(_right_of(node))

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
    line1.append(str(_value_of(node)))
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
                _add_left(node, _new_node(value))
                break
            node = left_child
        else:
            right_child = _right_of(node)
            if right_child == _null:
                _add_right(node, _new_node(value))
                break
            node = right_child
        depth += 1
    return depth


def _random_insert(root, value):
    """Insert a node randomly into the tree."""
    depth = 1
    node = root
    while True:
        if random() < 0.5:
            left_child = _left_of(node)
            if left_child == _null:
                _add_left(node, _new_node(value))
                break
            node = left_child
        else:
            right_child = _right_of(node)
            if right_child == _null:
                _add_right(node, _new_node(value))
                break
            node = right_child
        depth += 1
    return depth


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


def _generate_values(height, multiplier=1):
    """Generate and return a list of random node values."""
    if not isinstance(height, int) or height < 0:
        raise ValueError('Height must be a non-negative integer')
    count = 2 ** (height + 1) - 1
    return sample(range(count * multiplier), count)


def setup(node_class,
          node_init_func,
          null_value,
          value_attr,
          left_attr,
          right_attr):
    """Set up a custom specification for the binary tree node.

    :param node_class: the binary tree node class
    :param node_init_func: node initializer function which takes the node
        value as the only argument and returns an instance of node_class
    :param null_value: the null/sentinel value
    :param value_attr: the attribute name reserved for the node value
    :param left_attr: the attribute name reserved for the left child
    :param right_attr: the attribute name reserved for the right child
    :raises ValueError: if an invalid set of arguments is given
    """
    global _node_cls
    global _node_init_func
    global _null
    global _value_attr
    global _left_attr
    global _right_attr

    # Do some sanity checking on the arguments
    if not inspect_.isclass(node_class):
        raise ValueError('Invalid class given for the node')
    try:
        node = node_init_func(2 if null_value == 1 else 1)
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
    _node_init_func = node_init_func
    _null = null_value
    _value_attr = value_attr
    _left_attr = left_attr
    _right_attr = right_attr


def tree(height=4, balanced=False):
    """Generate a random binary tree and return its root.

    :param height: the height of the tree (default: 4)
    :param balanced: whether the tree is weight-balanced (default: False)
    :return: the root of the generated binary tree
    """
    values = _generate_values(height)
    if balanced:
        return _build_tree(values)

    root = _new_node(values[0])
    for index in range(1, len(values)):
        depth = _random_insert(root, values[index])
        if depth == height:
            break
    return root


def bst(height=4):
    """Generate a random binary search tree and return its root.

    :param height: the height of the tree (default: 4)
    :return: the root of the generated binary search tree
    """
    values = _generate_values(height)
    root = _new_node(values[0])
    for index in range(1, len(values)):
        depth = _bst_insert(root, values[index])
        if depth == height:
            break
    return root


def heap(height=4, max=False):
    """Generate a random min/max heap and return its root.

    :param height: the height of the tree (default: 4)
    :param max: whether to generate a max or min heap
    :return: the root of the generated heap
    """
    values = _generate_values(height)
    if max:
        negated = [-v for v in values]
        heapify(negated)
        return _build_tree([-v for v in negated])
    else:
        heapify(values)
        return _build_tree(values)


def stringify(bt):
    """Return the string representation of the binary tree.

    :param bt: the binary tree
    :return: the string representation
    """
    if bt == _null:
        return ''
    elif _is_list(bt):
        if not bt:
            return ''
        bt = _build_tree(bt)
    elif _is_node(bt):
        _validate_tree(bt)
    else:
        raise ValueError('Expecting a list or a node')
    return '\n' + '\n'.join(_build_str(bt)[0])


def pprint(bt):
    """Pretty print the binary tree.

    :param bt: the binary tree to pretty print
    :raises ValueError: if an invalid tree is given
    """
    print(stringify(bt))


def convert(bt):
    """Convert a binary tree into a list, or vice versa.

    :param bt: the binary tree to convert
    :return: the converted form of the binary tree
    :raises ValueError: if an invalid tree is given
    """
    if bt == _null:
        return []
    if _is_list(bt):
        return _build_tree(bt)
    elif _is_node(bt):
        _validate_tree(bt)
        return _build_list(bt)
    raise ValueError('Expecting a list or a node')


def inspect(bt):
    """Return the properties of the binary tree.

    :param bt: the binary tree to inspect
    :return: the properties of the binary tree
    :raises ValueError: if an invalid tree is given
    """
    if _is_list(bt):
        bt = _build_tree(bt)
    elif _is_node(bt):
        _validate_tree(bt)
    else:
        raise ValueError('Expecting a list or a node')

    is_full = True
    is_bst = True
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
                    is_bst = False
                elif _value_of(left_child) < node_value:
                    is_ascending = False
                next_nodes.append(left_child)
                num_of_children +=1

            if right_child != _null:
                if _value_of(right_child) > node_value:
                    is_descending = False
                elif _value_of(right_child) < node_value:
                    is_ascending = False
                    is_bst = False
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
        'is_bst': is_bst,
        'height': current_depth,
        'leaf_count': leaf_count,
        'node_count': node_count,
        'min_leaf_depth': min_leaf_depth,
        'max_leaf_depth': current_depth,
        'min_value': min_value,
        'max_value': max_value,
        'is_full': is_full
    }
