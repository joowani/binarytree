import xml.etree.ElementTree as ET

from binarytree.layout import _get_coords, generate_svg


def test_get_coords():
    values = [0, 6, 5, None, 1, 4, 2]
    assert _get_coords(values) == (
        [(0, 0, 0), (0, 1, 6), (1, 1, 5), (1, 2, 1), (2, 2, 4), (3, 2, 2)],
        [(0, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 2), (1, 1, 2, 2), (1, 1, 3, 2)],
    )


def test_svg():
    svg = generate_svg([0, 1, 2])
    svg_tree = ET.fromstring(svg)
    assert svg_tree.tag == "{http://www.w3.org/2000/svg}svg"
