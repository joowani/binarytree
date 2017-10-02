import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from random import randint

import pytest

from binarytree import (
    Node,
    convert,
    get_level,
    get_levels,
    inspect,
    tree,
    bst,
    heap,
    subtree,
    prune,
    leafs,
    pprint,
    show,
    show_ids,
    show_all,
    stringify,
    customize,
)

repetitions = 100


class CaptureOutput(list):
    def __enter__(self):
        self._orig_stdout = sys.stdout
        self._temp_stdout = StringIO()
        sys.stdout = self._temp_stdout
        return self

    def __exit__(self, *args):
        self.extend(self._temp_stdout.getvalue().splitlines())
        sys.stdout = self._orig_stdout


def attr(instance, attributes):
    result = instance
    for attribute in attributes.split('.'):
        result = getattr(result, attribute)
    return result


@pytest.mark.order1
def test_node():
    node = Node(1)
    assert attr(node, 'left') is None
    assert attr(node, 'right') is None
    assert attr(node, 'value') == 1
    assert attr(node, 'parent') is None
    assert repr(node) == 'Node(1)'

    node.left = Node(2)
    node.right = Node(3)
    assert repr(attr(node, 'left')) == 'Node(2)'
    assert repr(attr(node, 'right')) == 'Node(3)'
    assert attr(node.left, 'parent') == node
    assert attr(node.right, 'parent') == node

    node.left.left = Node(4)
    node.left.right = Node(5)
    node.right.left = Node(6)
    node.right.right = Node(7)
    assert repr(attr(node, 'left.left')) == 'Node(4)'
    assert repr(attr(node, 'left.right')) == 'Node(5)'
    assert repr(attr(node, 'right.right')) == 'Node(7)'
    assert repr(attr(node, 'right.left')) == 'Node(6)'
    assert attr(node.left.left, 'parent') == node.left
    assert attr(node.left.right, 'parent') == node.left
    assert attr(node.right.left, 'parent') == node.right
    assert attr(node.right.right, 'parent') == node.right

    assert node.is_root() is True
    assert node.left.is_root() is False
    assert node.left.right.is_leaf() is True
    assert node.is_leaf() is False

    assert node.level() == 0
    assert node.right.level() == 1


@pytest.mark.order2
def test_tree():
    for invalid_height in ['foo', -1]:
        with pytest.raises(ValueError) as err:
            tree(height=invalid_height)
        assert str(err.value) == 'Height must be a non-negative integer'

    for _ in range(repetitions):
        root = tree(height=0)
        assert attr(root, 'left') is None
        assert attr(root, 'right') is None
        assert isinstance(attr(root, 'value'), int)
        assert inspect(root)['height'] == 0
        assert inspect(root)['is_height_balanced'] is True
        assert inspect(root)['is_weight_balanced'] is True

    for _ in range(repetitions):
        height = randint(1, 10)
        root = tree(height)
        nodes_to_visit = [root]
        while nodes_to_visit:
            node = nodes_to_visit.pop()
            assert isinstance(node, Node)
            assert isinstance(attr(node, 'value'), int)
            if attr(node, 'left') is not None:
                nodes_to_visit.append(attr(node, 'left'))
            if attr(node, 'right') is not None:
                nodes_to_visit.append(attr(node, 'right'))
        assert inspect(root)['height'] == height

    for _ in range(repetitions):
        height = randint(1, 10)
        root = tree(height, is_balanced=True)
        nodes_to_visit = [root]
        while nodes_to_visit:
            node = nodes_to_visit.pop()
            assert isinstance(node, Node)
            assert isinstance(attr(node, 'value'), int)
            if attr(node, 'left') is not None:
                nodes_to_visit.append(attr(node, 'left'))
            if attr(node, 'right') is not None:
                nodes_to_visit.append(attr(node, 'right'))
        assert inspect(root)['height'] == height
        assert inspect(root)['is_height_balanced'] is True
        assert inspect(root)['is_weight_balanced'] is True


def test_bst():
    for invalid_height in ['foo', -1]:
        with pytest.raises(ValueError) as err:
            bst(height=invalid_height)
        assert str(err.value) == 'Height must be a non-negative integer'

    for _ in range(repetitions):
        root = bst(height=0)
        assert attr(root, 'left') is None
        assert attr(root, 'right') is None
        assert isinstance(attr(root, 'value'), int)
        assert inspect(root)['height'] == 0
        assert inspect(root)['is_bst'] is True

    for _ in range(repetitions):
        height = randint(1, 10)
        root = bst(height)
        nodes_to_visit = [root]
        while nodes_to_visit:
            node = nodes_to_visit.pop()
            assert isinstance(node, Node)
            assert isinstance(attr(node, 'value'), int)
            if attr(node, 'left') is not None:
                nodes_to_visit.append(attr(node, 'left'))
            if attr(node, 'right') is not None:
                nodes_to_visit.append(attr(node, 'right'))
        assert inspect(root)['height'] == height
        assert inspect(root)['is_bst'] is True


def test_heap():
    for invalid_height in ['foo', -1]:
        with pytest.raises(ValueError) as err:
            heap(height=invalid_height)
        assert str(err.value) == 'Height must be a non-negative integer'

    # Test heap generation with height of 0
    for _ in range(repetitions):
        root = heap(height=0)
        assert attr(root, 'left') is None
        assert attr(root, 'right') is None
        assert isinstance(attr(root, 'value'), int)
        assert inspect(root)['height'] == 0
        assert inspect(root)['is_min_heap'] is True
        assert inspect(root)['is_max_heap'] is True

    for _ in range(repetitions):
        height = randint(1, 10)
        root = heap(height)
        nodes_to_visit = [root]
        while nodes_to_visit:
            node = nodes_to_visit.pop()
            assert isinstance(node, Node)
            assert isinstance(attr(node, 'value'), int)
            if attr(node, 'left') is not None:
                nodes_to_visit.append(attr(node, 'left'))
            if attr(node, 'right') is not None:
                nodes_to_visit.append(attr(node, 'right'))
        assert inspect(root)['height'] == height
        assert inspect(root)['is_min_heap'] is True

    for _ in range(repetitions):
        height = randint(1, 10)
        root = heap(height, is_max=True)
        nodes_to_visit = [root]
        while nodes_to_visit:
            node = nodes_to_visit.pop()
            assert isinstance(node, Node)
            assert isinstance(attr(node, 'value'), int)
            if attr(node, 'left') is not None:
                nodes_to_visit.append(attr(node, 'left'))
            if attr(node, 'right') is not None:
                nodes_to_visit.append(attr(node, 'right'))
        assert inspect(root)['height'] == height
        assert inspect(root)['is_max_heap'] is True


def test_convert():
    for invalid_argument in [1, 'foo', int]:
        with pytest.raises(ValueError) as err:
            convert(invalid_argument)
        assert str(err.value) == 'Expecting a list or a node'

    assert convert(None) == []

    # Convert trees to lists
    for convert_func in [convert, lambda node: node.convert()]:
        root = Node(1)
        assert convert_func(root) == [1]

        root.right = Node(3)
        assert convert_func(root) == [1, None, 3]

        root.left = Node(2)
        assert convert_func(root) == [1, 2, 3]

        root.left.right = Node(4)
        assert convert_func(root) == [1, 2, 3, None, 4]

        root.right.left = Node(5)
        assert convert_func(root) == [1, 2, 3, None, 4, 5]

        root.right.right = Node(6)
        assert convert_func(root) == [1, 2, 3, None, 4, 5, 6]

        root.right.right = Node(None)
        with pytest.raises(ValueError) as err:
            convert_func(root)
        assert str(err.value) == 'A node cannot have a null value'

        root.right.right = {}
        with pytest.raises(ValueError) as err:
            assert convert_func(root)
        assert str(err.value) == 'Found an invalid node in the tree'

    # Convert lists to trees
    with pytest.raises(ValueError) as err:
        convert([None, 2, 3])
    assert str(err.value) == 'Node missing at index 0'

    with pytest.raises(ValueError) as err:
        convert([1, 2, None, 3, 4, 5, 6])
    assert str(err.value) == 'Node missing at index 2'

    assert convert([]) is None

    bt = convert([1])
    assert attr(bt, 'value') == 1
    assert attr(bt, 'left') is None
    assert attr(bt, 'right') is None

    bt = convert([1, 2])
    assert attr(bt, 'value') == 1
    assert attr(bt, 'left.value') == 2
    assert attr(bt, 'right') is None
    assert attr(bt, 'left.left') is None
    assert attr(bt, 'left.right') is None

    bt = convert([1, None, 3])
    assert attr(bt, 'value') == 1
    assert attr(bt, 'left') is None
    assert attr(bt, 'right.value') == 3
    assert attr(bt, 'right.left') is None
    assert attr(bt, 'right.right') is None

    bt = convert([1, 2, 3])
    assert attr(bt, 'value') == 1
    assert attr(bt, 'left.value') == 2
    assert attr(bt, 'right.value') == 3
    assert attr(bt, 'left.left') is None
    assert attr(bt, 'left.right') is None
    assert attr(bt, 'right.left') is None
    assert attr(bt, 'right.right') is None


def test_get_levels():
    for invalid_argument in [None, 1, 'foo']:
        with pytest.raises(ValueError) as err:
            get_levels(invalid_argument)
        assert str(err.value) == 'Expecting a list or a node'
    assert str(get_levels(convert([0, 1, 2]))) == '[[Node(0)], [Node(1), Node(2)]]'
    assert str(get_levels(convert([0, 1, 2]), show_values=True)) == '[[0], [1, 2]]'
    assert str(get_levels(convert([0, 1]), show_values=True, show_nulls=True))\
        == '[[0], [1, None]]'


def test_get_level():
    for invalid_argument in [None, 1, 'foo']:
        with pytest.raises(ValueError) as err:
            get_level(invalid_argument, 0)
        assert str(err.value) == 'Expecting a list or a node'
    for invalid_argument in [None, -1, 'foo']:
        with pytest.raises(ValueError) as err:
            get_level(convert([0, 1, 2]), invalid_argument)
        assert str(err.value) == 'Requested level must be a non-negative integer.'
    with pytest.raises(ValueError) as err:
        get_level(convert([0, 1, 2]), 2)
    assert str(err.value) == 'Requested level not present in tree.'

    assert str(get_level(convert([0, 1, 2]), 1)) == '[Node(1), Node(2)]'
    assert str(get_level(convert([0, 1, 2]), 1, show_values=True)) == '[1, 2]'
    assert str(get_level(convert([0, 1, 2, 3]), 2, show_values=True, show_nulls=True))\
        == '[3, None, None, None]'


def test_inspect():
    for invalid_argument in [None, 1, 'foo']:
        with pytest.raises(ValueError) as err:
            inspect(invalid_argument)
        assert str(err.value) == 'Expecting a list or a node'

    def convert_inspect(target):
        return inspect(convert(target))

    def self_inspect(target):
        return target.inspect()

    for inspect_func in [inspect, convert_inspect, self_inspect]:
        root = Node(1)
        assert inspect_func(root) == {
            'is_height_balanced': True,
            'is_weight_balanced': True,
            'is_max_heap': True,
            'is_min_heap': True,
            'is_bst': True,
            'is_full': True,
            'height': 0,
            'max_value': 1,
            'min_value': 1,
            'leaf_count': 1,
            'node_count': 1,
            'max_leaf_depth': 0,
            'min_leaf_depth': 0,
        }
        root.left = Node(2)
        assert inspect_func(root) == {
            'is_height_balanced': True,
            'is_weight_balanced': True,
            'is_max_heap': False,
            'is_min_heap': True,
            'is_bst': False,
            'is_full': False,
            'height': 1,
            'max_value': 2,
            'min_value': 1,
            'node_count': 2,
            'leaf_count': 1,
            'max_leaf_depth': 1,
            'min_leaf_depth': 1,
        }
        root.right = Node(3)
        assert inspect_func(root) == {
            'is_height_balanced': True,
            'is_weight_balanced': True,
            'is_max_heap': False,
            'is_min_heap': True,
            'is_bst': False,
            'is_full': True,
            'height': 1,
            'max_value': 3,
            'min_value': 1,
            'leaf_count': 2,
            'node_count': 3,
            'max_leaf_depth': 1,
            'min_leaf_depth': 1,
        }
        root.value = 2
        root.left.value = 1
        root.right.value = 3
        assert inspect_func(root) == {
            'is_height_balanced': True,
            'is_weight_balanced': True,
            'is_max_heap': False,
            'is_min_heap': False,
            'is_bst': True,
            'is_full': True,
            'height': 1,
            'max_value': 3,
            'min_value': 1,
            'leaf_count': 2,
            'node_count': 3,
            'max_leaf_depth': 1,
            'min_leaf_depth': 1,
        }
        root.value = 1
        root.left.value = 2
        root.right.value = 3
        root.left.right = Node(4)
        assert inspect_func(root) == {
            'is_height_balanced': True,
            'is_weight_balanced': True,
            'is_max_heap': False,
            'is_min_heap': False,
            'is_bst': False,
            'is_full': False,
            'height': 2,
            'max_value': 4,
            'min_value': 1,
            'leaf_count': 2,
            'node_count': 4,
            'max_leaf_depth': 2,
            'min_leaf_depth': 1,
        }
        root.left.left = Node(5)
        assert inspect_func(root) == {
            'is_height_balanced': True,
            'is_weight_balanced': True,
            'is_max_heap': False,
            'is_min_heap': True,
            'is_bst': False,
            'is_full': True,
            'height': 2,
            'max_value': 5,
            'min_value': 1,
            'leaf_count': 3,
            'node_count': 5,
            'max_leaf_depth': 2,
            'min_leaf_depth': 1,
        }
        root.right.right = Node(6)
        assert inspect_func(root) == {
            'is_height_balanced': True,
            'is_weight_balanced': True,
            'is_max_heap': False,
            'is_min_heap': False,
            'is_bst': False,
            'is_full': False,
            'height': 2,
            'max_value': 6,
            'min_value': 1,
            'leaf_count': 3,
            'node_count': 6,
            'max_leaf_depth': 2,
            'min_leaf_depth': 2,
        }

        root.right.right = Node(None)
        with pytest.raises(ValueError) as err:
            assert inspect_func(root)
        assert str(err.value) == 'A node cannot have a null value'

        root.right.right = {}
        with pytest.raises(ValueError) as err:
            assert inspect_func(root)
        assert str(err.value) == 'Found an invalid node in the tree'


def test_show():
    def convert_show(target):
        show(convert(target))

    def convert_self_show(target):
        convert(target).show()

    for invalid_argument in [1, 'foo']:
        with pytest.raises(ValueError) as err:
            show(invalid_argument)
        assert str(err.value) == 'Expecting a list or a node'

    for show_func in [pprint, show, convert_show]:
        with CaptureOutput() as output:
            show_func([])
        assert output == ['']

    for show_func in [pprint, show, convert_show, convert_self_show]:
        with CaptureOutput() as output:
            show_func([1, 2])
        assert output == ['',
                          '  1',
                          ' / ',
                          '2  ',
                          '   '
                          ]

        with CaptureOutput() as output:
            show_func([1, None, 3])
        assert output == ['',
                          '1  ',
                          ' \\ ',
                          '  3',
                          '   '
                          ]

        with CaptureOutput() as output:
            show_func([1, 2, 3])
        assert output == ['',
                          '  1  ',
                          ' / \\ ',
                          '2   3',
                          '     '
                          ]

        with CaptureOutput() as output:
            show_func([1, 2, 3, None, 5])
        assert output == ['',
                          '  __1  ',
                          ' /   \\ ',
                          '2     3',
                          ' \\     ',
                          '  5    ',
                          '       '
                          ]
        with CaptureOutput() as output:
            show_func([1, 2, 3, None, 5, 6])
        assert output == ['',
                          '  __1__  ',
                          ' /     \\ ',
                          '2       3',
                          ' \\     / ',
                          '  5   6  ',
                          '         '
                          ]
        with CaptureOutput() as output:
            show_func([1, 2, 3, None, 5, 6, 7])
        assert output == ['',
                          '  __1__    ',
                          ' /     \\   ',
                          '2       3  ',
                          ' \\     / \\ ',
                          '  5   6   7',
                          '           '
                          ]
        with CaptureOutput() as output:
            show_func([1, 2, 3, 8, 5, 6, 7])
        assert output == ['',
                          '    __1__    ',
                          '   /     \\   ',
                          '  2       3  ',
                          ' / \\     / \\ ',
                          '8   5   6   7',
                          '             '
                          ]

    for _ in range(repetitions):
        bt = tree(height=10)
        with CaptureOutput() as output:
            show(bt)
        assert output == stringify(bt).splitlines()


def test_show_ids():
    def convert_show_ids(target):
        show_ids(convert(target))

    def convert_self_show_ids(target):
        convert(target).show_ids()

    for invalid_argument in [1, 'foo']:
        with pytest.raises(ValueError) as err:
            show_ids(invalid_argument)
        assert str(err.value) == 'Expecting a list or a node'

    for show_func in [show_ids, convert_show_ids]:
        with CaptureOutput() as output:
            show_func([])
        assert output == ['']

    for show_func in [show_ids, convert_show_ids, convert_self_show_ids]:
        with CaptureOutput() as output:
            show_func([1, 2])
        assert output == ['',
                          '  0',
                          ' / ',
                          '1  ',
                          '   '
                          ]

        with CaptureOutput() as output:
            show_func([1, None, 3])
        assert output == ['',
                          '0  ',
                          ' \\ ',
                          '  1',
                          '   '
                          ]

        with CaptureOutput() as output:
            show_func([1, 2, 3])
        assert output == ['',
                          '  0  ',
                          ' / \\ ',
                          '1   2',
                          '     '
                          ]

        with CaptureOutput() as output:
            show_func([1, 2, 3, None, 5])

        assert output == ['',
                          '  __0  ',
                          ' /   \\ ',
                          '1     2',
                          ' \\     ',
                          '  3    ',
                          '       '
                          ]
        with CaptureOutput() as output:
            show_func([1, 2, 3, None, 5, 6])
        assert output == ['',
                          '  __0__  ',
                          ' /     \\ ',
                          '1       2',
                          ' \\     / ',
                          '  3   4  ',
                          '         '
                          ]
        with CaptureOutput() as output:
            show_func([1, 2, 3, None, 5, 6, 7])
        assert output == ['',
                          '  __0__    ',
                          ' /     \\   ',
                          '1       2  ',
                          ' \\     / \\ ',
                          '  3   4   5',
                          '           '
                          ]
        with CaptureOutput() as output:
            show_func([1, 2, 3, 8, 5, 6, 7])
        assert output == ['',
                          '    __0__    ',
                          '   /     \\   ',
                          '  1       2  ',
                          ' / \\     / \\ ',
                          '3   4   5   6',
                          '             '
                          ]

    for _ in range(repetitions):
        bt = tree(height=10)
        with CaptureOutput() as output:
            show_ids(bt)
        assert output == stringify(bt, True, False).splitlines()


def test_show_all():
    def convert_show_all(target):
        show_all(convert(target))

    def convert_self_show_all(target):
        convert(target).show_all()

    for invalid_argument in [1, 'foo']:
        with pytest.raises(ValueError) as err:
            show_all(invalid_argument)
        assert str(err.value) == 'Expecting a list or a node'

    for show_func in [show_all, convert_show_all]:
        with CaptureOutput() as output:
            show_func([])
        assert output == ['']

    for show_func in [show_all, convert_show_all, convert_self_show_all]:
        with CaptureOutput() as output:
            show_func([1, 2])
        assert output == ['',
                          '   _0:1',
                          '  /    ',
                          '1:2    ',
                          '       '
                          ]

        with CaptureOutput() as output:
            show_func([1, None, 3])
        assert output == ['',
                          '0:1_   ',
                          '    \\  ',
                          '    1:3',
                          '       '
                          ]

        with CaptureOutput() as output:
            show_func([1, 2, 3])
        assert output == ['',
                          '   _0:1_   ',
                          '  /     \\  ',
                          '1:2     2:3',
                          '           '
                          ]

        with CaptureOutput() as output:
            show_func([1, 2, 3, None, 5])
        assert output == ['',
                          '   _____0:1_   ',
                          '  /         \\  ',
                          '1:2_        2:3',
                          '    \\          ',
                          '    3:5        ',
                          '               '
                          ]

        with CaptureOutput() as output:
            show_func([1, 2, 3, None, 5, 6])
        assert output == ['',
                          '   _____0:1_____   ',
                          '  /             \\  ',
                          '1:2_           _2:3',
                          '    \\         /    ',
                          '    3:5     4:6    ',
                          '                   '
                          ]
        with CaptureOutput() as output:
            show_func([1, 2, 3, None, 5, 6, 7])
        assert output == ['',
                          '   _____0:1_____       ',
                          '  /             \\      ',
                          '1:2_           _2:3_   ',
                          '    \\         /     \\  ',
                          '    3:5     4:6     5:7',
                          '                       '
                          ]
        with CaptureOutput() as output:
            show_func([1, 2, 3, 8, 5, 6, 7])
        assert output == ['',
                          '       _____0:1_____       ',
                          '      /             \\      ',
                          '   _1:2_           _2:3_   ',
                          '  /     \\         /     \\  ',
                          '3:8     4:5     5:6     6:7',
                          '                           '
                          ]
    for _ in range(repetitions):
        bt = tree(height=10)
        with CaptureOutput() as output:
            show_all(bt)
        assert output == stringify(bt, True, True).splitlines()


def test_subtree():

    def self_subtree(target, node_id):
        return target.subtree(node_id)

    for invalid_tree in ['foo', -1, None]:
        with pytest.raises(ValueError) as err:
            subtree(invalid_tree, 0)
        assert str(err.value) == 'Expecting a list or a node'

    for subtree_func in [subtree, self_subtree]:
        root = Node(1)

        for invalid_id in ['foo', None]:
            with pytest.raises(ValueError) as err:
                subtree_func(root, invalid_id)
            assert str(err.value) == 'The node ID must be an integer'

        with pytest.raises(ValueError) as err:
            subtree_func(root, -1)
        assert str(err.value) == 'The node ID must start from 0'

        assert subtree_func(root, 0) == root
        for invalid_id in [1, 2, 3, 4, 5]:
            with pytest.raises(ValueError) as err:
                subtree_func(root, invalid_id)
            assert str(err.value) == \
                'Cannot find node with ID {}'.format(invalid_id)

        root.left = Node(2)
        assert subtree_func(root, 0) == root
        assert subtree_func(root, 1) == root.left
        for invalid_id in [2, 3, 4, 5]:
            with pytest.raises(ValueError) as err:
                subtree_func(root, invalid_id)
            assert str(err.value) == \
                'Cannot find node with ID {}'.format(invalid_id)

        root.right = Node(3)
        assert subtree_func(root, 0) == root
        assert subtree_func(root, 1) == root.left
        assert subtree_func(root, 2) == root.right
        for invalid_id in [3, 4, 5]:
            with pytest.raises(ValueError) as err:
                subtree_func(root, invalid_id)
            assert str(err.value) == \
                'Cannot find node with ID {}'.format(invalid_id)

        root.left.right = Node(4)
        assert subtree_func(root, 0) == root
        assert subtree_func(root, 1) == root.left
        assert subtree_func(root, 2) == root.right
        assert subtree_func(root, 3) == root.left.right
        for invalid_id in [4, 5]:
            with pytest.raises(ValueError) as err:
                subtree_func(root, invalid_id)
            assert str(err.value) == \
                'Cannot find node with ID {}'.format(invalid_id)

        root.left.left = Node(5)
        assert subtree_func(root, 0) == root
        assert subtree_func(root, 1) == root.left
        assert subtree_func(root, 2) == root.right
        assert subtree_func(root, 3) == root.left.left
        assert subtree_func(root, 4) == root.left.right
        for invalid_id in [5, 6]:
            with pytest.raises(ValueError) as err:
                subtree_func(root, invalid_id)
            assert str(err.value) == \
                'Cannot find node with ID {}'.format(invalid_id)


def test_prune():

    def self_prune(target, node_id):
        return target.prune(node_id)

    for invalid_tree in ['foo', -1, None]:
        with pytest.raises(ValueError) as err:
            prune(invalid_tree, 0)
        assert str(err.value) == 'Expecting a list or a node'

    for prune_func in [prune, self_prune]:
        root = Node(1)

        for bad_id in ['foo', None]:
            with pytest.raises(ValueError) as err:
                prune_func(root, bad_id)
            assert str(err.value) == 'The node ID must be an integer'

        with pytest.raises(ValueError) as err:
            prune_func(root, -1)
        assert str(err.value) == 'The node ID must start from 0'

        with pytest.raises(ValueError) as err:
            prune_func(root, 0)
        assert str(err.value) == 'Cannot prune the root node'

        with pytest.raises(ValueError) as err:
            prune_func(root, 10)
        assert str(err.value) == 'Cannot find node with ID 10'

        root.left = Node(2)
        assert prune_func(root, 1) == root
        assert root.left is None

        root.left = Node(2)
        root.right = Node(3)
        assert prune_func(root, 1) == root
        assert root.left is None
        assert attr(root, 'right.value') == 3

        root.left = Node(2)
        root.right = Node(3)
        root.left.left = Node(4)
        root.left.right = Node(5)
        root.left.right.left = Node(6)
        root.left.right.right = Node(7)

        assert prune_func(root.left.right, 2) == root.left.right
        assert attr(root, 'left.right.right') is None

        assert prune_func(root, 4) == root
        assert attr(root, 'left.right') is None

        assert prune_func(root, 1) == root
        assert attr(root, 'left') is None
        assert attr(root, 'right.value') == 3

        assert prune_func(root, 1) == root
        assert attr(root, 'right') is None


def test_leafs():

    def self_leafs(target, values_only):
        return target.leafs(values_only)

    def to_set(nodes):
        return set(attr(node, 'value') for node in nodes)

    for invalid_tree in ['foo', -1, None]:
        with pytest.raises(ValueError) as err:
            leafs(invalid_tree)
        assert str(err.value) == 'Expecting a list or a node'

    for leafs_func in [leafs, self_leafs]:
        root = Node(1)
        assert set(leafs_func(root, True)) == {1}
        assert to_set(leafs_func(root, False)) == {1}

        root.left = Node(2)
        assert set(leafs_func(root, True)) == {2}
        assert to_set(leafs_func(root, False)) == {2}

        root.right = Node(3)
        assert set(leafs_func(root, True)) == {2, 3}
        assert to_set(leafs_func(root, False)) == {2, 3}

        root.left.left = Node(4)
        assert set(leafs_func(root, True)) == {3, 4}
        assert to_set(leafs_func(root, False)) == {3, 4}

        root.left.right = Node(5)
        assert set(leafs_func(root, True)) == {3, 4, 5}
        assert to_set(leafs_func(root, False)) == {3, 4, 5}


def test_customize():
    null = -1

    class GoodNode(Node):

        def __init__(self, val, bar=-1, baz=-1):
            self.foo = val
            self.bar = bar
            self.baz = baz

    class BadNode1(object):

        def __init__(self, val, bar=-1, baz=-1):
            self.foo = val
            self.bar = bar
            self.baz = baz

    class BadNode2(object):

        def __init__(self, val, bar=-2, baz=-2):
            self.foo = val
            self.bar = bar
            self.baz = baz

    customize(
        node_init=lambda v: GoodNode(v),
        node_class=GoodNode,
        null_value=null,
        value_attr='foo',
        left_attr='bar',
        right_attr='baz'
    )
    for _ in range(repetitions):
        nodes_to_visit = [tree(height=10)]
        while nodes_to_visit:
            node = nodes_to_visit.pop()

            # Check that the new node class is used
            assert isinstance(node, GoodNode)

            # Check that the original attributes do not exist
            assert not hasattr(node, 'left')
            assert not hasattr(node, 'right')
            assert not hasattr(node, 'value')

            # Check that the new attributes are as expected
            left = attr(node, 'bar')
            right = attr(node, 'baz')
            value = attr(node, 'foo')
            assert isinstance(value, int)

            if left != null:
                assert isinstance(left, GoodNode)
                nodes_to_visit.append(left)
            if right != null:
                assert isinstance(right, GoodNode)
                nodes_to_visit.append(right)

    customize(
        node_init=lambda v: GoodNode(v),
        node_class=GoodNode,
        null_value=null,
        value_attr='foo',
        left_attr='bar',
        right_attr='baz'
    )
    for _ in range(repetitions):
        nodes_to_visit = [tree(height=10)]
        while nodes_to_visit:
            node = nodes_to_visit.pop()

            # Check that the new node class is used
            assert isinstance(node, GoodNode)

            # Check that the original attributes do not exist
            assert not hasattr(node, 'left')
            assert not hasattr(node, 'right')
            assert not hasattr(node, 'value')

            # Check that the new attributes are as expected
            left = attr(node, 'bar')
            right = attr(node, 'baz')
            value = attr(node, 'foo')
            assert isinstance(value, int)

            if left != null:
                assert isinstance(left, GoodNode)
                nodes_to_visit.append(left)
            if right != null:
                assert isinstance(right, GoodNode)
                nodes_to_visit.append(right)

    with pytest.raises(ValueError) as err:
        customize(
            node_init=lambda v: BadNode1(v),
            node_class=None,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='baz',
        )
    assert 'Invalid class given' in str(err.value)

    with pytest.raises(ValueError) as err:
        customize(
            node_init=None,
            node_class=BadNode1,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='baz',
        )
    assert 'function must be a callable' in str(err.value)

    with pytest.raises(ValueError) as err:
        customize(
            node_init=lambda v: GoodNode(v),
            node_class=BadNode1,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='baz',
        )
    assert 'returns an instance of "BadNode1"' in str(err.value)

    with pytest.raises(ValueError) as err:
        customize(
            node_init=lambda v: GoodNode(v),
            node_class=GoodNode,
            null_value=-1,
            value_attr='value',
            left_attr='bar',
            right_attr='baz',
        )
    assert 'required attributes "value"' in str(err.value)

    with pytest.raises(ValueError) as err:
        customize(
            node_init=lambda v: GoodNode(v),
            node_class=GoodNode,
            null_value=-1,
            value_attr='foo',
            left_attr='left',
            right_attr='baz',
        )
    assert 'required attributes "left"' in str(err.value)

    with pytest.raises(ValueError) as err:
        customize(
            node_init=lambda v: GoodNode(v),
            node_class=GoodNode,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='right',
        )
    assert 'required attributes "right"' in str(err.value)

    with pytest.raises(ValueError) as err:
        customize(
            node_init=lambda v: GoodNode(v),
            node_class=GoodNode,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='right',
        )
    assert 'required attributes "right"' in str(err.value)

    with pytest.raises(ValueError) as err:
        customize(
            node_init=lambda v: BadNode2(v, -2),
            node_class=BadNode2,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='baz',
        )
    assert (
               'expected null/sentinel value "-1" for its '
               'left child node attribute "bar"'
           ) in str(err.value)

    with pytest.raises(ValueError) as err:
        customize(
            node_init=lambda v: BadNode2(v, -1, -2),
            node_class=BadNode2,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='baz',
        )
    assert (
               'expected null/sentinel value "-1" for its '
               'right child node attribute "baz"'
           ) in str(err.value)
