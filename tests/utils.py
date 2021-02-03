from __future__ import absolute_import, unicode_literals

import sys

try:
    # noinspection PyCompatibility
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from binarytree import build


class CaptureOutput(list):
    """Context manager to catch stdout."""

    def __enter__(self):
        self._original_stdout = sys.stdout
        self._temp_stdout = StringIO()
        sys.stdout = self._temp_stdout
        return self

    def __exit__(self, *args):
        lines = self._temp_stdout.getvalue().splitlines()
        self.extend(line.rstrip() for line in lines)
        sys.stdout = self._original_stdout


def pprint_default(values):
    """Helper function for testing Node.pprint with default arguments."""
    root = build(values)
    with CaptureOutput() as output:
        root.pprint(index=False, delimiter="-")
    assert output[0] == "" and output[-1] == ""
    return [line for line in output if line != ""]


def pprint_with_index(values):
    """Helper function for testing Node.pprint with indexes."""
    root = build(values)
    with CaptureOutput() as output:
        root.pprint(index=True, delimiter=":")
    assert output[0] == "" and output[-1] == ""
    return [line for line in output if line != ""]


def builtin_print(values):
    """Helper function for testing builtin print on Node."""
    root = build(values)
    with CaptureOutput() as output:
        print(root)
    assert output[0] == "" and output[-1] == ""
    return [line for line in output if line != ""]
