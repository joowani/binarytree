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
    inspect,
    tree,
    bst,
    heap,
    pprint,
    stringify,
    setup as setup_node,
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
    assert repr(node) == 'Node(1)'


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
        root = tree(height, balanced=True)
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
        root = heap(height, max=True)
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
    for convert_func in [convert, lambda node: node.to_list()]:

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
            assert convert_func(root)
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
            'is_full' : False,
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
            'is_full' : True,
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
            'is_full' : True,
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
            'is_full' : False,
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
            'is_full' : True,
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
            'is_full' : False,
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


def test_print():

    def convert_print(target):
        print(convert(target))

    def convert_pprint(target):
        pprint(convert(target))

    for invalid_argument in [1, 'foo']:
        with pytest.raises(ValueError) as err:
            pprint(invalid_argument)
        assert str(err.value) == 'Expecting a list or a node'

    for print_func in [pprint, convert_pprint]:
        with CaptureOutput() as output:
            print_func([])
        assert output == ['']

    for print_func in [convert_print, pprint, convert_pprint]:
        with CaptureOutput() as output:
            print_func([1, 2])
        assert output == ['', '  1', ' / ', '2  ', '   ']

        with CaptureOutput() as output:
            print_func([1, None, 3])
        assert output == ['', '1  ', ' \\ ', '  3', '   ']

        with CaptureOutput() as output:
            print_func([1, 2, 3])
        assert output == ['', '  1  ', ' / \\ ', '2   3', '     ']

        with CaptureOutput() as output:
            print_func([1, 2, 3, None, 5])
        assert output == [
            '', '  __1  ', ' /   \\ ', '2     3',
            ' \\     ', '  5    ', '       '
        ]
        with CaptureOutput() as output:
            print_func([1, 2, 3, None, 5, 6])
        assert output == [
            '', '  __1__  ', ' /     \\ ',
            '2       3', ' \\     / ',
            '  5   6  ', '         '
        ]
        with CaptureOutput() as output:
            print_func([1, 2, 3, None, 5, 6, 7])
        assert output == [
            '', '  __1__    ', ' /     \\   ',
            '2       3  ', ' \\     / \\ ',
            '  5   6   7', '           '
        ]
        with CaptureOutput() as output:
            print_func([1, 2, 3, 8, 5, 6, 7])
        assert output == [
            '', '    __1__    ', '   /     \\   ',
            '  2       3  ', ' / \\     / \\ ',
            '8   5   6   7', '             '
        ]
    for _ in range(repetitions):
        bt = tree(height=10)
        with CaptureOutput() as output1:
            print(bt)
        assert output1 == str(bt).splitlines()
        assert output1 == stringify(bt).splitlines()


def test_setup():
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

    setup_node(
        node_init_func=lambda v: GoodNode(v),
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

    setup_node(
        node_init_func=lambda v: GoodNode(v),
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
        setup_node(
            node_init_func=lambda v: BadNode1(v),
            node_class=None,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='baz',
        )
    assert 'Invalid class given' in str(err.value)

    with pytest.raises(ValueError) as err:
        setup_node(
            node_init_func=None,
            node_class=BadNode1,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='baz',
        )
    assert 'function must be a callable' in str(err.value)

    with pytest.raises(ValueError) as err:
        setup_node(
            node_init_func=lambda v: GoodNode(v),
            node_class=BadNode1,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='baz',
        )
    assert 'returns an instance of "BadNode1"' in str(err.value)

    with pytest.raises(ValueError) as err:
        setup_node(
            node_init_func=lambda v: GoodNode(v),
            node_class=GoodNode,
            null_value=-1,
            value_attr='value',
            left_attr='bar',
            right_attr='baz',
        )
    assert 'required attributes "value"' in str(err.value)

    with pytest.raises(ValueError) as err:
        setup_node(
            node_init_func=lambda v: GoodNode(v),
            node_class=GoodNode,
            null_value=-1,
            value_attr='foo',
            left_attr='left',
            right_attr='baz',
        )
    assert 'required attributes "left"' in str(err.value)

    with pytest.raises(ValueError) as err:
        setup_node(
            node_init_func=lambda v: GoodNode(v),
            node_class=GoodNode,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='right',
        )
    assert 'required attributes "right"' in str(err.value)

    with pytest.raises(ValueError) as err:
        setup_node(
            node_init_func=lambda v: GoodNode(v),
            node_class=GoodNode,
            null_value=-1,
            value_attr='foo',
            left_attr='bar',
            right_attr='right',
        )
    assert 'required attributes "right"' in str(err.value)

    with pytest.raises(ValueError) as err:
        setup_node(
            node_init_func=lambda v: BadNode2(v, -2),
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
        setup_node(
            node_init_func=lambda v: BadNode2(v, -1, -2),
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
