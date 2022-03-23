from __future__ import absolute_import, unicode_literals

import sys
from typing import Any, List

try:
    # noinspection PyCompatibility
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from binarytree import NodeValueList, build


class CaptureOutput(List[str]):
    """Context manager to catch stdout."""

    def __enter__(self) -> "CaptureOutput":
        self._original_stdout = sys.stdout
        self._temp_stdout = StringIO()
        sys.stdout = self._temp_stdout
        return self

    def __exit__(self, *args: Any) -> None:
        lines = self._temp_stdout.getvalue().splitlines()
        self.extend(line.rstrip() for line in lines)
        sys.stdout = self._original_stdout


def pprint_default(values: NodeValueList) -> List[str]:
    """Helper function for testing Node.pprint with default arguments."""
    root = build(values)
    assert root is not None

    with CaptureOutput() as output:
        root.pprint(index=False, delimiter="-")
    assert output[0] == "" and output[-1] == ""
    return [line for line in output if line != ""]


def pprint_with_index(values: NodeValueList) -> List[str]:
    """Helper function for testing Node.pprint with indexes."""
    root = build(values)
    assert root is not None

    with CaptureOutput() as output:
        root.pprint(index=True, delimiter=":")
    assert output[0] == "" and output[-1] == ""
    return [line for line in output if line != ""]


def builtin_print(values: NodeValueList) -> List[str]:
    """Helper function for testing builtin print on Node."""
    root = build(values)
    assert root is not None

    with CaptureOutput() as output:
        print(root)
    assert output[0] == "" and output[-1] == ""
    return [line for line in output if line != ""]
