from __future__ import absolute_import, unicode_literals

import copy
import random
from typing import Any, List, Optional

import pytest

from binarytree import (
    Node,
    bst,
    build,
    build2,
    get_index,
    get_parent,
    heap,
    number_to_letters,
    tree,
)
from binarytree.exceptions import (
    NodeIndexError,
    NodeModifyError,
    NodeNotFoundError,
    NodeReferenceError,
    NodeTypeError,
    NodeValueError,
    TreeHeightError,
)
from tests.utils import builtin_print, pprint_default, pprint_with_index

REPETITIONS = 20

EXPECTED_SVG_XML_SINGLE_NODE = """
<svg width="48" height="96" xmlns="http://www.w3.org/2000/svg">
<style>
    .value {
        font: 300 16px sans-serif;
        text-align: center;
        dominant-baseline: middle;
        text-anchor: middle;
    }
    .node {
        fill: lightgray;
        stroke-width: 1;
    }
</style>
<g stroke="#000000">
<circle class="node" cx="17.0" cy="48" r="16"/>
<text class="value" x="17.0" y="48">0</text>
</g>
</svg>
"""

EXPECTED_SVG_XML_MULTIPLE_NODES = """
<svg width="192" height="192" xmlns="http://www.w3.org/2000/svg">
<style>
    .value {
        font: 300 16px sans-serif;
        text-align: center;
        dominant-baseline: middle;
        text-anchor: middle;
    }
    .node {
        fill: lightgray;
        stroke-width: 1;
    }
</style>
<g stroke="#000000">
<line x1="137.0" y1="96" x2="161.0" y2="144"/>
<line x1="41.0" y1="96" x2="17.0" y2="144"/>
<line x1="89.0" y1="48" x2="137.0" y2="96"/>
<line x1="89.0" y1="48" x2="41.0" y2="96"/>
<circle class="node" cx="89.0" cy="48" r="16"/>
<text class="value" x="89.0" y="48">0</text>
<circle class="node" cx="41.0" cy="96" r="16"/>
<text class="value" x="41.0" y="96">1</text>
<circle class="node" cx="137.0" cy="96" r="16"/>
<text class="value" x="137.0" y="96">2</text>
<circle class="node" cx="17.0" cy="144" r="16"/>
<text class="value" x="17.0" y="144">3</text>
<circle class="node" cx="161.0" cy="144" r="16"/>
<text class="value" x="161.0" y="144">4</text>
</g>
</svg>
"""
EMPTY_LIST: List[Optional[int]] = []


def test_node_init_and_setattr_with_integers() -> None:
    root = Node(1)
    assert root.left is None
    assert root.right is None
    assert root.val == 1
    assert root.value == 1
    assert repr(root) == "Node(1)"

    root.value = 2
    assert root.value == 2
    assert root.val == 2
    assert repr(root) == "Node(2)"

    root.val = 1
    assert root.value == 1
    assert root.val == 1
    assert repr(root) == "Node(1)"

    left_child = Node(2)
    root.left = left_child
    assert root.left is left_child
    assert root.right is None
    assert root.val == 1
    assert root.left.left is None
    assert root.left.right is None
    assert root.left.val == 2
    assert repr(left_child) == "Node(2)"

    right_child = Node(3)
    root.right = right_child
    assert root.left is left_child
    assert root.right is right_child
    assert root.val == 1
    assert root.right.left is None
    assert root.right.right is None
    assert root.right.val == 3
    assert repr(right_child) == "Node(3)"

    last_node = Node(4)
    left_child.right = last_node
    assert root.left.right is last_node
    assert repr(root.left.right) == "Node(4)"


def test_node_init_and_setattr_with_floats() -> None:
    root = Node(1.5)
    assert root.left is None
    assert root.right is None
    assert root.val == 1.5
    assert root.value == 1.5
    assert repr(root) == "Node(1.5)"

    root.value = 2.5
    assert root.value == 2.5
    assert root.val == 2.5
    assert repr(root) == "Node(2.5)"

    root.val = 1.5
    assert root.value == 1.5
    assert root.val == 1.5
    assert repr(root) == "Node(1.5)"

    left_child = Node(2.5)
    root.left = left_child
    assert root.left is left_child
    assert root.right is None
    assert root.val == 1.5
    assert root.left.left is None
    assert root.left.right is None
    assert root.left.val == 2.5
    assert repr(left_child) == "Node(2.5)"

    right_child = Node(3.5)
    root.right = right_child
    assert root.left is left_child
    assert root.right is right_child
    assert root.val == 1.5
    assert root.right.left is None
    assert root.right.right is None
    assert root.right.val == 3.5
    assert repr(right_child) == "Node(3.5)"

    last_node = Node(4.5)
    left_child.right = last_node
    assert root.left.right is last_node
    assert repr(root.left.right) == "Node(4.5)"


def test_node_init_and_setattr_with_letters() -> None:
    root = Node("A")
    assert root.left is None
    assert root.right is None
    assert root.val == "A"
    assert root.value == "A"
    assert repr(root) == "Node(A)"

    root.value = "B"
    assert root.value == "B"
    assert root.val == "B"
    assert repr(root) == "Node(B)"

    root.val = "A"
    assert root.value == "A"
    assert root.val == "A"
    assert repr(root) == "Node(A)"

    left_child = Node("B")
    root.left = left_child
    assert root.left is left_child
    assert root.right is None
    assert root.val == "A"
    assert root.left.left is None
    assert root.left.right is None
    assert root.left.val == "B"
    assert repr(left_child) == "Node(B)"

    right_child = Node("C")
    root.right = right_child
    assert root.left is left_child
    assert root.right is right_child
    assert root.val == "A"
    assert root.right.left is None
    assert root.right.right is None
    assert root.right.val == "C"
    assert repr(right_child) == "Node(C)"

    last_node = Node("D")
    left_child.right = last_node
    assert root.left.right is last_node
    assert repr(root.left.right) == "Node(D)"


def test_node_init_and_setattr_error_cases() -> None:
    root, left_child, right_child = Node(1), Node(2), Node(3)
    root.left = left_child
    root.right = right_child

    with pytest.raises(NodeValueError) as err1:
        Node(EMPTY_LIST)
    assert str(err1.value) == "node value must be a float/int/str"

    with pytest.raises(NodeValueError) as err2:
        Node(1).val = EMPTY_LIST
    assert str(err2.value) == "node value must be a float/int/str"

    with pytest.raises(NodeTypeError) as err3:
        Node(1, "this_is_not_a_node")  # type: ignore
    assert str(err3.value) == "left child must be a Node instance"

    with pytest.raises(NodeTypeError) as err4:
        Node(1, Node(1), "this_is_not_a_node")  # type: ignore
    assert str(err4.value) == "right child must be a Node instance"

    with pytest.raises(NodeTypeError) as err5:
        root.left = "this_is_not_a_node"  # type: ignore
    assert root.left is left_child
    assert str(err5.value) == "left child must be a Node instance"

    with pytest.raises(NodeTypeError) as err6:
        root.right = "this_is_not_a_node"  # type: ignore
    assert root.right is right_child
    assert str(err6.value) == "right child must be a Node instance"


def test_tree_equals_with_integers() -> None:
    root1 = Node(1)
    root2 = Node(1)
    assert root1.equals(None) is False  # type: ignore
    assert root1.equals(1) is False  # type: ignore
    assert root1.equals(Node(2)) is False
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True

    root1.left = Node(2)
    assert root1.equals(root2) is False
    assert root2.equals(root1) is False

    root2.left = Node(2)
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True

    root1.right = Node(3)
    assert root1.equals(root2) is False
    assert root2.equals(root1) is False

    root2.right = Node(3)
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True

    root1.right.left = Node(4)
    assert root1.equals(root2) is False
    assert root2.equals(root1) is False

    root2.right.left = Node(4)
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True


def test_tree_equals_with_floats() -> None:
    root1 = Node(1.5)
    root2 = Node(1.5)
    assert root1.equals(None) is False  # type: ignore
    assert root1.equals(1.5) is False  # type: ignore
    assert root1.equals(Node(2.5)) is False
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True

    root1.left = Node(2.5)
    assert root1.equals(root2) is False
    assert root2.equals(root1) is False

    root2.left = Node(2.5)
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True

    root1.right = Node(3.5)
    assert root1.equals(root2) is False
    assert root2.equals(root1) is False

    root2.right = Node(3.5)
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True

    root1.right.left = Node(4.5)
    assert root1.equals(root2) is False
    assert root2.equals(root1) is False

    root2.right.left = Node(4.5)
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True


def test_tree_equals_with_letters() -> None:
    root1 = Node("A")
    root2 = Node("A")
    assert root1.equals(None) is False  # type: ignore
    assert root1.equals("A") is False  # type: ignore
    assert root1.equals(Node("B")) is False
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True

    root1.left = Node("B")
    assert root1.equals(root2) is False
    assert root2.equals(root1) is False

    root2.left = Node("B")
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True

    root1.right = Node("C")
    assert root1.equals(root2) is False
    assert root2.equals(root1) is False

    root2.right = Node("C")
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True

    root1.right.left = Node("D")
    assert root1.equals(root2) is False
    assert root2.equals(root1) is False

    root2.right.left = Node("D")
    assert root1.equals(root2) is True
    assert root2.equals(root1) is True


def test_tree_clone_with_numbers() -> None:
    for _ in range(REPETITIONS):
        root = tree(letters=False)
        assert root is not None
        clone = root.clone()
        assert root.values == clone.values
        assert root.equals(clone)
        assert clone.equals(root)
        assert root.properties == clone.properties


def test_tree_clone_with_letters() -> None:
    for _ in range(REPETITIONS):
        root = tree(letters=True)
        assert root is not None
        clone = root.clone()
        assert root.values == clone.values
        assert root.equals(clone)
        assert clone.equals(root)
        assert root.properties == clone.properties


def test_list_representation_1() -> None:
    root = build(EMPTY_LIST)
    assert root is None

    root = build([1])
    assert root is not None
    assert root.val == 1
    assert root.left is None
    assert root.right is None

    root = build([1, 2])
    assert root is not None
    assert root.val == 1
    assert root.left is not None
    assert root.left.val == 2
    assert root.right is None

    root = build([1, 2, 3])
    assert root is not None
    assert root.val == 1
    assert root.left is not None
    assert root.left.val == 2
    assert root.right is not None
    assert root.right.val == 3
    assert root.left.left is None
    assert root.left.right is None
    assert root.right.left is None
    assert root.right.right is None

    root = build([1, 2, 3, None, 4])
    assert root is not None
    assert root.val == 1
    assert root.left is not None
    assert root.left.val == 2
    assert root.right is not None
    assert root.right.val == 3
    assert root.left.left is None
    assert root.left.right is not None
    assert root.left.right.val == 4
    assert root.right.left is None
    assert root.right.right is None
    assert root.left.right.left is None
    assert root.left.right.right is None

    with pytest.raises(NodeNotFoundError) as err:
        build([None, 1, 2])
    assert str(err.value) == "parent node missing at index 0"

    with pytest.raises(NodeNotFoundError) as err:
        build([1, None, 2, 3, 4])
    assert str(err.value) == "parent node missing at index 1"

    root = Node(1)
    assert root.values == [1]

    root.right = Node(3)
    assert root.values == [1, None, 3]

    root.left = Node(2)
    assert root.values == [1, 2, 3]

    root.right.left = Node(4)
    assert root.values == [1, 2, 3, None, None, 4]

    root.right.right = Node(5)
    assert root.values == [1, 2, 3, None, None, 4, 5]

    root.left.left = Node(6)
    assert root.values == [1, 2, 3, 6, None, 4, 5]

    root.left.right = Node(7)
    assert root.values == [1, 2, 3, 6, 7, 4, 5]

    for _ in range(REPETITIONS):
        t1 = tree()
        assert t1 is not None

        t2 = build(t1.values)
        assert t2 is not None

        assert t1.values == t2.values


def test_list_representation_2() -> None:
    root = build2(EMPTY_LIST)
    assert root is None

    root = build2([1])
    assert root is not None
    assert root.val == 1
    assert root.left is None
    assert root.right is None

    root = build2([1, 2])
    assert root is not None
    assert root.val == 1
    assert root.left is not None
    assert root.left.val == 2
    assert root.right is None

    root = build2([1, 2, 3])
    assert root is not None
    assert root.val == 1
    assert root.left is not None
    assert root.left.val == 2
    assert root.right is not None
    assert root.right.val == 3
    assert root.left.left is None
    assert root.left.right is None
    assert root.right.left is None
    assert root.right.right is None

    root = build2([1, 2, 3, None, 4])
    assert root is not None
    assert root.val == 1
    assert root.left is not None
    assert root.left.val == 2
    assert root.right is not None
    assert root.right.val == 3
    assert root.left.left is None
    assert root.left.right is not None
    assert root.left.right.val == 4
    assert root.right.left is None
    assert root.right.right is None
    assert root.left.right.left is None
    assert root.left.right.right is None

    root = build2([1, None, 2, 3, 4])
    assert root is not None
    assert root.val == 1
    assert root.left is None
    assert root.right is not None
    assert root.right.val == 2
    assert root.right.left is not None
    assert root.right.left.val == 3
    assert root.right.right is not None
    assert root.right.right.val == 4

    root = build2([2, 5, None, 3, None, 1, 4])
    assert root is not None
    assert root.val == 2
    assert root.left is not None
    assert root.left.val == 5
    assert root.right is None
    assert root.left.left is not None
    assert root.left.left.val == 3
    assert root.left.left.left is not None
    assert root.left.left.left.val == 1
    assert root.left.left.right is not None
    assert root.left.left.right.val == 4

    with pytest.raises(NodeValueError):
        build2([None, 1, 2])

    root = Node(1)
    assert root.values2 == [1]
    root.right = Node(3)
    assert root.values2 == [1, None, 3]
    root.left = Node(2)
    assert root.values2 == [1, 2, 3]
    root.right.left = Node(4)
    assert root.values2 == [1, 2, 3, None, None, 4]
    root.right.right = Node(5)
    assert root.values2 == [1, 2, 3, None, None, 4, 5]
    root.left.left = Node(6)
    assert root.values2 == [1, 2, 3, 6, None, 4, 5]
    root.left.right = Node(7)
    assert root.values2 == [1, 2, 3, 6, 7, 4, 5]

    root = Node(1)
    assert root.values2 == [1]
    root.left = Node(2)
    assert root.values2 == [1, 2]
    root.right = Node(3)
    assert root.values2 == [1, 2, 3]
    root.right = None
    root.left.left = Node(3)
    assert root.values2 == [1, 2, None, 3]
    root.left.left.left = Node(4)
    assert root.values2 == [1, 2, None, 3, None, 4]
    root.left.left.right = Node(5)
    assert root.values2 == [1, 2, None, 3, None, 4, 5]

    for _ in range(REPETITIONS):
        t1 = tree()
        assert t1 is not None

        t2 = build2(t1.values2)
        assert t2 is not None

        assert t1.values2 == t2.values2


def test_tree_get_node_by_level_order_index() -> None:
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.left.right.left = Node(6)

    assert root[0] is root
    assert root[1] is root.left
    assert root[2] is root.right
    assert root[3] is root.left.left
    assert root[4] is root.left.right
    assert root[9] is root.left.right.left

    for index in [5, 6, 7, 8, 10]:
        with pytest.raises(NodeNotFoundError) as err1:
            assert root[index]
        assert str(err1.value) == "node missing at index {}".format(index)

    with pytest.raises(NodeIndexError) as err2:
        assert root[-1]
    assert str(err2.value) == "node index must be a non-negative int"


def test_tree_set_node_by_level_order_index() -> None:
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.left.right.left = Node(6)

    new_node_1 = Node(7)
    new_node_2 = Node(8)
    new_node_3 = Node(9)

    with pytest.raises(NodeModifyError) as err1:
        root[0] = new_node_1
    assert str(err1.value) == "cannot modify the root node"

    with pytest.raises(NodeIndexError) as err2:
        root[-1] = new_node_1
    assert str(err2.value) == "node index must be a non-negative int"

    with pytest.raises(NodeNotFoundError) as err3:
        root[100] = new_node_1
    assert str(err3.value) == "parent node missing at index 49"

    root[10] = new_node_1
    assert root.val == 1
    assert root.left.val == 2
    assert root.right.val == 3
    assert root.left.left.val == 4
    assert root.left.right.val == 5
    assert root.left.right.left.val == 6
    assert root.left.right.right is new_node_1

    root[4] = new_node_2
    assert root.val == 1
    assert root.left.val == 2
    assert root.right.val == 3
    assert root.left.left.val == 4
    assert root.left.right.val == 8
    assert root.left.right.left is None
    assert root.left.right.right is None

    root[1] = new_node_3
    root[2] = new_node_2
    assert root.left is new_node_3
    assert root.right is new_node_2


def test_tree_delete_node_by_level_order_index() -> None:
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.left.right.left = Node(6)

    with pytest.raises(NodeModifyError) as err1:
        del root[0]
    assert str(err1.value) == "cannot delete the root node"

    with pytest.raises(NodeIndexError) as err2:
        del root[-1]
    assert str(err2.value) == "node index must be a non-negative int"

    with pytest.raises(NodeNotFoundError) as err3:
        del root[10]
    assert str(err3.value) == "no node to delete at index 10"

    with pytest.raises(NodeNotFoundError) as err4:
        del root[100]
    assert str(err4.value) == "no node to delete at index 100"

    del root[3]
    assert root.left.left is None
    assert root.left.val == 2
    assert root.left.right.val == 5
    assert root.left.right.right is None
    assert root.left.right.left.val == 6
    assert root.left.right.left.left is None
    assert root.left.right.left.right is None
    assert root.right.val == 3
    assert root.right.left is None
    assert root.right.right is None
    assert root.size == 5

    del root[2]
    assert root.left.left is None
    assert root.left.val == 2
    assert root.left.right.val == 5
    assert root.left.right.right is None
    assert root.left.right.left.val == 6
    assert root.left.right.left.left is None
    assert root.left.right.left.right is None
    assert root.right is None
    assert root.size == 4

    del root[4]
    assert root.left.left is None
    assert root.left.right is None
    assert root.right is None
    assert root.size == 2

    del root[1]
    assert root.left is None
    assert root.right is None
    assert root.size == 1


def test_tree_print_with_integers_no_index() -> None:
    for printer in [builtin_print, pprint_default]:
        lines = printer([1])
        assert lines == ["1"]
        lines = printer([1, 2])
        assert lines == ["  1", " /", "2"]
        lines = printer([1, None, 3])
        assert lines == ["1", " \\", "  3"]
        lines = printer([1, 2, 3])
        assert lines == ["  1", " / \\", "2   3"]
        lines = printer([1, 2, 3, None, 5])
        assert lines == ["  __1", " /   \\", "2     3", " \\", "  5"]
        lines = printer([1, 2, 3, None, 5, 6])
        assert lines == ["  __1__", " /     \\", "2       3", " \\     /", "  5   6"]
        lines = printer([1, 2, 3, None, 5, 6, 7])
        assert lines == [
            "  __1__",
            " /     \\",
            "2       3",
            " \\     / \\",
            "  5   6   7",
        ]
        lines = printer([1, 2, 3, 8, 5, 6, 7])
        assert lines == [
            "    __1__",
            "   /     \\",
            "  2       3",
            " / \\     / \\",
            "8   5   6   7",
        ]


def test_tree_print_with_integers_with_index() -> None:
    lines = pprint_with_index([1])
    assert lines == ["0:1"]
    lines = pprint_with_index([1, 2])
    assert lines == ["   _0:1", "  /", "1:2"]
    lines = pprint_with_index([1, None, 3])
    assert lines == ["0:1_", "    \\", "    2:3"]
    lines = pprint_with_index([1, 2, 3])
    assert lines == ["   _0:1_", "  /     \\", "1:2     2:3"]
    lines = pprint_with_index([1, 2, 3, None, 5])
    assert lines == [
        "   _____0:1_",
        "  /         \\",
        "1:2_        2:3",
        "    \\",
        "    4:5",
    ]
    lines = pprint_with_index([1, 2, 3, None, 5, 6])
    assert lines == [
        "   _____0:1_____",
        "  /             \\",
        "1:2_           _2:3",
        "    \\         /",
        "    4:5     5:6",
    ]
    lines = pprint_with_index([1, 2, 3, None, 5, 6, 7])
    assert lines == [
        "   _____0:1_____",
        "  /             \\",
        "1:2_           _2:3_",
        "    \\         /     \\",
        "    4:5     5:6     6:7",
    ]
    lines = pprint_with_index([1, 2, 3, 8, 5, 6, 7])
    assert lines == [
        "       _____0:1_____",
        "      /             \\",
        "   _1:2_           _2:3_",
        "  /     \\         /     \\",
        "3:8     4:5     5:6     6:7",
    ]


def test_tree_print_with_letters_no_index() -> None:
    for printer in [builtin_print, pprint_default]:
        lines = printer(["A"])
        assert lines == ["A"]
        lines = printer(["A", "B"])
        assert lines == ["  A", " /", "B"]
        lines = printer(["A", None, "C"])
        assert lines == ["A", " \\", "  C"]
        lines = printer(["A", "B", "C"])
        assert lines == ["  A", " / \\", "B   C"]
        lines = printer(["A", "B", "C", None, "E"])
        assert lines == ["  __A", " /   \\", "B     C", " \\", "  E"]
        lines = printer(["A", "B", "C", None, "E", "F"])
        assert lines == ["  __A__", " /     \\", "B       C", " \\     /", "  E   F"]
        lines = printer(["A", "B", "C", None, "E", "F", "G"])
        assert lines == [
            "  __A__",
            " /     \\",
            "B       C",
            " \\     / \\",
            "  E   F   G",
        ]
        lines = printer(["A", "B", "C", "D", "E", "F", "G"])
        assert lines == [
            "    __A__",
            "   /     \\",
            "  B       C",
            " / \\     / \\",
            "D   E   F   G",
        ]


def test_tree_print_with_letters_with_index() -> None:
    lines = pprint_with_index(["A"])
    assert lines == ["0:A"]
    lines = pprint_with_index(["A", "B"])
    assert lines == ["   _0:A", "  /", "1:B"]
    lines = pprint_with_index(["A", None, "C"])
    assert lines == ["0:A_", "    \\", "    2:C"]
    lines = pprint_with_index(["A", "B", "C"])
    assert lines == ["   _0:A_", "  /     \\", "1:B     2:C"]
    lines = pprint_with_index(["A", "B", "C", None, "E"])
    assert lines == [
        "   _____0:A_",
        "  /         \\",
        "1:B_        2:C",
        "    \\",
        "    4:E",
    ]
    lines = pprint_with_index(["A", "B", "C", None, "E", "F"])
    assert lines == [
        "   _____0:A_____",
        "  /             \\",
        "1:B_           _2:C",
        "    \\         /",
        "    4:E     5:F",
    ]
    lines = pprint_with_index(["A", "B", "C", None, "E", "F", "G"])
    assert lines == [
        "   _____0:A_____",
        "  /             \\",
        "1:B_           _2:C_",
        "    \\         /     \\",
        "    4:E     5:F     6:G",
    ]
    lines = pprint_with_index(["A", "B", "C", "D", "E", "F", "G"])
    assert lines == [
        "       _____0:A_____",
        "      /             \\",
        "   _1:B_           _2:C_",
        "  /     \\         /     \\",
        "3:D     4:E     5:F     6:G",
    ]


def test_tree_validate() -> None:
    class TestNode(Node):
        def __setattr__(self, attr: str, value: Any) -> None:
            object.__setattr__(self, attr, value)

    root = Node(1)
    root.validate()  # Should pass

    root = Node(1)
    root.left = Node(2)
    root.validate()  # Should pass

    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.validate()  # Should pass

    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.left.right.left = Node(6)
    root.validate()  # Should pass

    root = TestNode(1)
    root.left = "not_a_node"  # type: ignore
    with pytest.raises(NodeTypeError) as err1:
        root.validate()
    assert str(err1.value) == "invalid node instance at index 1"

    root = TestNode(1)
    root.right = TestNode(2)
    root.right.val = EMPTY_LIST
    with pytest.raises(NodeValueError) as err2:
        root.validate()
    assert str(err2.value) == "invalid node value at index 2"

    root = TestNode(1)
    root.left = TestNode(2)
    root.left.right = root
    with pytest.raises(NodeReferenceError) as err3:
        root.validate()
    assert str(err3.value) == "cyclic reference at Node(1) (level-order index 4)"


def test_tree_validate_with_letters() -> None:
    class TestNode(Node):
        def __setattr__(self, attr: str, value: Any) -> None:
            object.__setattr__(self, attr, value)

    root = Node("A")
    root.validate()  # Should pass

    root = Node("A")
    root.left = Node("B")
    root.validate()  # Should pass

    root = Node("A")
    root.left = Node("B")
    root.right = Node(3)
    root.validate()  # Should pass

    root = Node("A")
    root.left = Node("B")
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.left.right.left = Node(6)
    root.validate()  # Should pass

    root = TestNode("A")
    root.left = "not_a_node"  # type: ignore
    with pytest.raises(NodeTypeError) as err1:
        root.validate()
    assert str(err1.value) == "invalid node instance at index 1"

    root = TestNode("A")
    root.right = TestNode("B")
    root.right.val = EMPTY_LIST
    with pytest.raises(NodeValueError) as err2:
        root.validate()
    assert str(err2.value) == "invalid node value at index 2"

    root = TestNode("A")
    root.left = TestNode("B")
    root.left.right = root
    with pytest.raises(NodeReferenceError) as err3:
        root.validate()
    assert str(err3.value) == "cyclic reference at Node(A) (level-order index 4)"


def test_tree_properties() -> None:
    root = Node(1)
    assert root.properties == {
        "height": 0,
        "is_balanced": True,
        "is_bst": True,
        "is_complete": True,
        "is_max_heap": True,
        "is_min_heap": True,
        "is_perfect": True,
        "is_strict": True,
        "is_symmetric": True,
        "leaf_count": 1,
        "max_leaf_depth": 0,
        "max_node_value": 1,
        "min_leaf_depth": 0,
        "min_node_value": 1,
        "size": 1,
    }
    assert root.height == 0
    assert root.is_balanced is True
    assert root.is_bst is True
    assert root.is_complete is True
    assert root.is_max_heap is True
    assert root.is_min_heap is True
    assert root.is_perfect is True
    assert root.is_strict is True
    assert root.is_symmetric is True
    assert root.leaf_count == 1
    assert root.max_leaf_depth == 0
    assert root.max_node_value == 1
    assert root.min_leaf_depth == 0
    assert root.min_node_value == 1
    assert root.size == len(root) == 1

    root.left = Node(2)
    assert root.properties == {
        "height": 1,
        "is_balanced": True,
        "is_bst": False,
        "is_complete": True,
        "is_max_heap": False,
        "is_min_heap": True,
        "is_perfect": False,
        "is_strict": False,
        "is_symmetric": False,
        "leaf_count": 1,
        "max_leaf_depth": 1,
        "max_node_value": 2,
        "min_leaf_depth": 1,
        "min_node_value": 1,
        "size": 2,
    }
    assert root.height == 1
    assert root.is_balanced is True
    assert root.is_bst is False
    assert root.is_complete is True
    assert root.is_max_heap is False
    assert root.is_min_heap is True
    assert root.is_perfect is False
    assert root.is_strict is False
    assert root.is_symmetric is False
    assert root.leaf_count == 1
    assert root.max_leaf_depth == 1
    assert root.max_node_value == 2
    assert root.min_leaf_depth == 1
    assert root.min_node_value == 1
    assert root.size == len(root) == 2

    root.right = Node(3)
    assert root.properties == {
        "height": 1,
        "is_balanced": True,
        "is_bst": False,
        "is_complete": True,
        "is_max_heap": False,
        "is_min_heap": True,
        "is_perfect": True,
        "is_strict": True,
        "is_symmetric": False,
        "leaf_count": 2,
        "max_leaf_depth": 1,
        "max_node_value": 3,
        "min_leaf_depth": 1,
        "min_node_value": 1,
        "size": 3,
    }
    assert root.height == 1
    assert root.is_balanced is True
    assert root.is_bst is False
    assert root.is_complete is True
    assert root.is_max_heap is False
    assert root.is_min_heap is True
    assert root.is_perfect is True
    assert root.is_strict is True
    assert root.is_symmetric is False
    assert root.leaf_count == 2
    assert root.max_leaf_depth == 1
    assert root.max_node_value == 3
    assert root.min_leaf_depth == 1
    assert root.min_node_value == 1
    assert root.size == len(root) == 3

    root.left.left = Node(4)
    assert root.properties == {
        "height": 2,
        "is_balanced": True,
        "is_bst": False,
        "is_complete": True,
        "is_max_heap": False,
        "is_min_heap": True,
        "is_perfect": False,
        "is_strict": False,
        "is_symmetric": False,
        "leaf_count": 2,
        "max_leaf_depth": 2,
        "max_node_value": 4,
        "min_leaf_depth": 1,
        "min_node_value": 1,
        "size": 4,
    }
    assert root.height == 2
    assert root.is_balanced is True
    assert root.is_bst is False
    assert root.is_complete is True
    assert root.is_max_heap is False
    assert root.is_min_heap is True
    assert root.is_perfect is False
    assert root.is_strict is False
    assert root.is_symmetric is False
    assert root.leaf_count == 2
    assert root.max_leaf_depth == 2
    assert root.max_node_value == 4
    assert root.min_leaf_depth == 1
    assert root.min_node_value == 1
    assert root.size == len(root) == 4

    root.right.left = Node(5)
    assert root.properties == {
        "height": 2,
        "is_balanced": True,
        "is_bst": False,
        "is_complete": False,
        "is_max_heap": False,
        "is_min_heap": False,
        "is_perfect": False,
        "is_strict": False,
        "is_symmetric": False,
        "leaf_count": 2,
        "max_leaf_depth": 2,
        "max_node_value": 5,
        "min_leaf_depth": 2,
        "min_node_value": 1,
        "size": 5,
    }
    assert root.height == 2
    assert root.is_balanced is True
    assert root.is_bst is False
    assert root.is_complete is False
    assert root.is_max_heap is False
    assert root.is_min_heap is False
    assert root.is_perfect is False
    assert root.is_strict is False
    assert root.is_symmetric is False
    assert root.leaf_count == 2
    assert root.max_leaf_depth == 2
    assert root.max_node_value == 5
    assert root.min_leaf_depth == 2
    assert root.min_node_value == 1
    assert root.size == len(root) == 5

    root.right.left.left = Node(6)
    assert root.properties == {
        "height": 3,
        "is_balanced": False,
        "is_bst": False,
        "is_complete": False,
        "is_max_heap": False,
        "is_min_heap": False,
        "is_perfect": False,
        "is_strict": False,
        "is_symmetric": False,
        "leaf_count": 2,
        "max_leaf_depth": 3,
        "max_node_value": 6,
        "min_leaf_depth": 2,
        "min_node_value": 1,
        "size": 6,
    }
    assert root.height == 3
    assert root.is_balanced is False
    assert root.is_bst is False
    assert root.is_complete is False
    assert root.is_max_heap is False
    assert root.is_min_heap is False
    assert root.is_perfect is False
    assert root.is_strict is False
    assert root.is_symmetric is False
    assert root.leaf_count == 2
    assert root.max_leaf_depth == 3
    assert root.max_node_value == 6
    assert root.min_leaf_depth == 2
    assert root.min_node_value == 1
    assert root.size == len(root) == 6

    root.left.left.left = Node(7)
    assert root.properties == {
        "height": 3,
        "is_balanced": False,
        "is_bst": False,
        "is_complete": False,
        "is_max_heap": False,
        "is_min_heap": False,
        "is_perfect": False,
        "is_strict": False,
        "is_symmetric": False,
        "leaf_count": 2,
        "max_leaf_depth": 3,
        "max_node_value": 7,
        "min_leaf_depth": 3,
        "min_node_value": 1,
        "size": 7,
    }
    assert root.height == 3
    assert root.is_balanced is False
    assert root.is_bst is False
    assert root.is_complete is False
    assert root.is_max_heap is False
    assert root.is_min_heap is False
    assert root.is_perfect is False
    assert root.is_strict is False
    assert root.is_symmetric is False
    assert root.leaf_count == 2
    assert root.max_leaf_depth == 3
    assert root.max_node_value == 7
    assert root.min_leaf_depth == 3
    assert root.min_node_value == 1
    assert root.size == len(root) == 7


def test_tree_traversal() -> None:
    n1 = Node(1)
    assert n1.levels == [[n1]]
    assert n1.leaves == [n1]
    assert n1.inorder == [n1]
    assert n1.preorder == [n1]
    assert n1.postorder == [n1]
    assert n1.levelorder == [n1]

    n2 = Node(2)
    n1.left = n2
    assert n1.levels == [[n1], [n2]]
    assert n1.leaves == [n2]
    assert n1.inorder == [n2, n1]
    assert n1.preorder == [n1, n2]
    assert n1.postorder == [n2, n1]
    assert n1.levelorder == [n1, n2]

    n3 = Node(3)
    n1.right = n3
    assert n1.levels == [[n1], [n2, n3]]
    assert n1.leaves == [n2, n3]
    assert n1.inorder == [n2, n1, n3]
    assert n1.preorder == [n1, n2, n3]
    assert n1.postorder == [n2, n3, n1]
    assert n1.levelorder == [n1, n2, n3]

    n4 = Node(4)
    n5 = Node(5)
    n2.left = n4
    n2.right = n5

    assert n1.levels == [[n1], [n2, n3], [n4, n5]]
    assert n1.leaves == [n3, n4, n5]
    assert n1.inorder == [n4, n2, n5, n1, n3]
    assert n1.preorder == [n1, n2, n4, n5, n3]
    assert n1.postorder == [n4, n5, n2, n3, n1]
    assert n1.levelorder == [n1, n2, n3, n4, n5]


def test_tree_generation() -> None:
    for invalid_height in ["foo", -1, None]:
        with pytest.raises(TreeHeightError) as err:
            tree(height=invalid_height)  # type: ignore
        assert str(err.value) == "height must be an int between 0 - 9"

    root = tree(height=0)
    assert root is not None

    root.validate()
    assert root.height == 0
    assert root.left is None
    assert root.right is None
    assert isinstance(root.val, int)

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)

        root = tree(random_height)
        assert root is not None

        root.validate()
        assert root.height == random_height

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)

        root = tree(random_height, is_perfect=True)
        assert root is not None

        root.validate()
        assert root.height == random_height
        assert root.is_perfect is True
        assert root.is_balanced is True
        assert root.is_strict is True


def test_bst_generation() -> None:
    for invalid_height in ["foo", -1, None]:
        with pytest.raises(TreeHeightError) as err:
            bst(height=invalid_height)  # type: ignore
        assert str(err.value) == "height must be an int between 0 - 9"

    root = bst(height=0)
    assert root is not None
    root.validate()
    assert root.height == 0
    assert root.left is None
    assert root.right is None
    assert isinstance(root.val, int)

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = bst(random_height)
        assert root is not None
        root.validate()
        assert root.is_bst is True
        assert root.height == random_height

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = bst(random_height, letters=True)
        assert root is not None
        root.validate()
        assert root.is_bst is True
        assert root.height == random_height

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = bst(random_height, is_perfect=True)
        assert root is not None
        root.validate()
        assert root.height == random_height

        if not root.is_bst:
            raise Exception("boo")

        assert root.is_bst is True
        assert root.is_perfect is True
        assert root.is_balanced is True
        assert root.is_strict is True

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = bst(random_height, letters=True, is_perfect=True)
        assert root is not None
        root.validate()
        assert root.height == random_height

        if not root.is_bst:
            raise Exception("boo")

        assert root.is_bst is True
        assert root.is_perfect is True
        assert root.is_balanced is True
        assert root.is_strict is True


def test_heap_generation() -> None:
    for invalid_height in ["foo", -1, None]:
        with pytest.raises(TreeHeightError) as err:
            heap(height=invalid_height)  # type: ignore
        assert str(err.value) == "height must be an int between 0 - 9"

    root = heap(height=0)
    assert root is not None
    root.validate()
    assert root.height == 0
    assert root.left is None
    assert root.right is None
    assert isinstance(root.val, int)

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = heap(random_height, is_max=True)
        assert root is not None
        root.validate()
        assert root.is_max_heap is True
        assert root.is_min_heap is False
        assert root.height == random_height

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = heap(random_height, letters=True, is_max=True)
        assert root is not None
        root.validate()
        assert root.is_max_heap is True
        assert root.is_min_heap is False
        assert root.height == random_height

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = heap(random_height, is_max=False)
        assert root is not None
        root.validate()
        assert root.is_max_heap is False
        assert root.is_min_heap is True
        assert root.height == random_height

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = heap(random_height, letters=True, is_max=False)
        assert root is not None
        root.validate()
        assert root.is_max_heap is False
        assert root.is_min_heap is True
        assert root.height == random_height

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = heap(random_height, is_perfect=True)
        assert root is not None
        root.validate()
        assert root.is_max_heap is True
        assert root.is_min_heap is False
        assert root.is_perfect is True
        assert root.is_balanced is True
        assert root.is_strict is True
        assert root.height == random_height

    for _ in range(REPETITIONS):
        random_height = random.randint(1, 9)
        root = heap(random_height, letters=True, is_perfect=True)
        assert root is not None
        root.validate()
        assert root.is_max_heap is True
        assert root.is_min_heap is False
        assert root.is_perfect is True
        assert root.is_balanced is True
        assert root.is_strict is True
        assert root.height == random_height


def test_heap_float_values() -> None:
    root = Node(1.0)
    root.left = Node(0.5)
    root.right = Node(1.5)

    assert root.height == 1
    assert root.is_balanced is True
    assert root.is_bst is True
    assert root.is_complete is True
    assert root.is_max_heap is False
    assert root.is_min_heap is False
    assert root.is_perfect is True
    assert root.is_strict is True
    assert root.leaf_count == 2
    assert root.max_leaf_depth == 1
    assert root.max_node_value == 1.5
    assert root.min_leaf_depth == 1
    assert root.min_node_value == 0.5
    assert root.size == 3

    for printer in [builtin_print, pprint_default]:
        lines = printer([1.0])
        assert lines == ["1.0"]
        lines = printer([1.0, 2.0])
        assert lines == ["   _1.0", "  /", "2.0"]
        lines = printer([1.0, None, 3.0])
        assert lines == ["1.0_", "    \\", "    3.0"]
        lines = printer([1.0, 2.0, 3.0])
        assert lines == ["   _1.0_", "  /     \\", "2.0     3.0"]
        lines = printer([1.0, 2.0, 3.0, None, 5.0])
        assert lines == [
            "   _____1.0_",
            "  /         \\",
            "2.0_        3.0",
            "    \\",
            "    5.0",
        ]


def test_heap_float_values_builders() -> None:
    for builder in [tree, bst, heap]:
        for _ in range(REPETITIONS):
            root = builder()  # type: ignore
            root_copy = copy.deepcopy(root)

            for node in root:
                node.value += 0.1

            assert root.height == root_copy.height
            assert root.is_balanced == root_copy.is_balanced
            assert root.is_bst == root_copy.is_bst
            assert root.is_complete == root_copy.is_complete
            assert root.is_max_heap == root_copy.is_max_heap
            assert root.is_min_heap == root_copy.is_min_heap
            assert root.is_perfect == root_copy.is_perfect
            assert root.is_strict == root_copy.is_strict
            assert root.is_symmetric == root_copy.is_symmetric
            assert root.leaf_count == root_copy.leaf_count
            assert root.max_leaf_depth == root_copy.max_leaf_depth
            assert root.max_node_value == root_copy.max_node_value + 0.1
            assert root.min_leaf_depth == root_copy.min_leaf_depth
            assert root.min_node_value == root_copy.min_node_value + 0.1
            assert root.size == root_copy.size


def test_get_index_utility_function() -> None:
    root = Node(0)
    root.left = Node(1)
    root.right = Node(2)
    root.left.left = Node(3)
    root.right.right = Node(4)

    assert get_index(root, root) == 0
    assert get_index(root, root.left) == 1
    assert get_index(root, root.right) == 2
    assert get_index(root, root.left.left) == 3
    assert get_index(root, root.right.right) == 6

    with pytest.raises(NodeReferenceError) as err1:
        get_index(root.left, root.right)
    assert str(err1.value) == "given nodes are not in the same tree"

    with pytest.raises(NodeTypeError) as err2:
        get_index(root, None)  # type: ignore
    assert str(err2.value) == "descendent must be a Node instance"

    with pytest.raises(NodeTypeError) as err3:
        get_index(None, root.left)  # type: ignore
    assert str(err3.value) == "root must be a Node instance"


def test_get_parent_utility_function() -> None:
    root = Node(0)
    root.left = Node(1)
    root.right = Node(2)
    root.left.left = Node(3)
    root.right.right = Node(4)

    assert get_parent(root, root.left.left) == root.left
    assert get_parent(root, root.left) == root
    assert get_parent(root, root) is None
    assert get_parent(root, root.right.right) == root.right
    assert get_parent(root, root.right) == root
    assert get_parent(root, Node(5)) is None
    assert get_parent(None, root.left) is None
    assert get_parent(root, None) is None


def test_svg_generation() -> None:
    root = Node(0)
    assert root.svg() == EXPECTED_SVG_XML_SINGLE_NODE

    root.left = Node(1)
    root.right = Node(2)
    root.left.left = Node(3)
    root.right.right = Node(4)
    assert root.svg() == EXPECTED_SVG_XML_MULTIPLE_NODES


def test_number_to_letters_utility_function() -> None:
    with pytest.raises(AssertionError):
        number_to_letters(-1)

    assert number_to_letters(0) == "A"
    assert number_to_letters(1) == "B"
    assert number_to_letters(25) == "Z"
    assert number_to_letters(26) == "ZA"
    assert number_to_letters(51) == "ZZ"
    assert number_to_letters(52) == "ZZA"

    for _ in range(REPETITIONS):
        num1 = random.randint(0, 1000)
        num2 = random.randint(0, 1000)
        str1 = number_to_letters(num1)
        str2 = number_to_letters(num2)
        assert (num1 < num2) == (str1 < str2)
        assert (num1 > num2) == (str1 > str2)
        assert (num1 == num2) == (str1 == str2)
