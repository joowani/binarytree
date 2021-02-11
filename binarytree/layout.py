""" Module containing layout related algorithms."""
from typing import List, Tuple, Union


def _get_coords(
    values: List[Union[float, int, None]]
) -> Tuple[
    List[Tuple[int, int, Union[float, int, None]]], List[Tuple[int, int, int, int]]
]:
    """Generate the coordinates used for rendering the nodes and edges.

    node and edges are stored as tuples in the form node: (x, y, label) and
    edge: (x1, y1, x2, y2)

    Each coordinate is relative y is the depth, x is the position of the node
    on a level from left to right 0 to 2**depth -1

    :param values: Values of the binary tree.
    :type values: list of ints
    :return: nodes and edges list
    :rtype: two lists of tuples

    """
    x = 0
    y = 0
    nodes = []
    edges = []

    # root node
    nodes.append((x, y, values[0]))
    # append other nodes and their edges
    y += 1
    for value in values[1:]:
        if value is not None:
            nodes.append((x, y, value))
            edges.append((x // 2, y - 1, x, y))
        x += 1
        # check if level is full
        if x == 2 ** y:
            x = 0
            y += 1
    return nodes, edges


def generate_svg(values: List[Union[float, int, None]]) -> str:
    """Generate a svg image from a binary tree

    A simple layout is used based on a perfect tree of same height in which all
    leaves would be regularly spaced.

    :param values: Values of the binary tree.
    :type values: list of ints
    :return: the svg image of the tree.
    :rtype: str
    """
    node_size = 16.0
    stroke_width = 1.5
    gutter = 0.5
    x_scale = (2 + gutter) * node_size
    y_scale = 3.0 * node_size

    # retrieve relative coordinates
    nodes, edges = _get_coords(values)
    y_min = min([n[1] for n in nodes])
    y_max = max([n[1] for n in nodes])

    # generate the svg string
    svg = f"""
    <svg width="{x_scale * 2**y_max}" height="{y_scale * (2 + y_max)}"
         xmlns="http://www.w3.org/2000/svg">
        <style>
            .bt-label {{
                font: 300 {node_size}px sans-serif;;
                text-align: center;
                dominant-baseline: middle;
                text-anchor: middle;
            }}
            .bt-node {{
                fill: lightgray;
                stroke-width: {stroke_width};
            }}

        </style>
        <g stroke="#111">
    """
    # scales

    def scalex(x: int, y: int) -> float:
        depth = y_max - y
        # offset
        x = 2 ** (depth + 1) * x + 2 ** depth - 1
        return 1 + node_size + x_scale * x / 2

    def scaley(y: int) -> float:
        return float(y_scale * (1 + y - y_min))

    # edges
    def svg_edge(x1: float, y1: float, x2: float, y2: float) -> str:
        """Generate svg code for an edge"""
        return f"""<line x1="{x1}" x2="{x2}" y1="{y1}" y2="{y2}"/>"""

    for a in edges:
        x1, y1, x2, y2 = a
        svg += svg_edge(scalex(x1, y1), scaley(y1), scalex(x2, y2), scaley(y2))

    # nodes
    def svg_node(x: float, y: float, label: str = "") -> str:
        """Generate svg code for a node and his label"""
        return f"""
            <circle class="bt-node" cx="{x}" cy="{y}" r="{node_size}"/>
            <text class="bt-label" x="{x}" y="{y}">{label}</text>"""

    for n in nodes:
        x, y, label = n
        svg += svg_node(scalex(x, y), scaley(y), str(label))

    svg += "</g></svg>"
    return svg
