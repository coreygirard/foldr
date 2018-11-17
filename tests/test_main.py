import doctest
import unittest

from hypothesis import given
from hypothesis.strategies import (builds, from_regex, integers, just, lists,
                                   recursive, tuples)

from src.main import *


def test__from_list():
    data = [(0, "aaa"), (1, "bbb"), (2, "ccc"), (1, "ddd"), (2, "eee"), (2, "fff")]

    result = from_list(data, simple=True)
    expected = [["aaa", [["bbb", [["ccc", []]]], ["ddd", [["eee", []], ["fff", []]]]]]]

    assert result == expected

    data = [(0, "aaa"), (1, "bbb"), (0, "ccc"), (1, "ddd")]

    result = from_list(data, simple=True)
    expected = [["aaa", [["bbb", []]]], ["ccc", [["ddd", []]]]]

    assert result == expected


def test__from_attribute():
    class Example(object):
        def __init__(self, depth, data):
            self.depth = depth
            self.data = data

    data = [
        Example(0, "aaa"),
        Example(1, "bbb"),
        Example(2, "ccc"),
        Example(1, "ddd"),
        Example(2, "eee"),
        Example(2, "fff"),
    ]

    result = from_attribute(data, "depth", simple=True)
    assert len(result) == 1

    assert result[0][0].data == "aaa"
    assert result[0][1][0][0].data == "bbb"
    assert result[0][1][0][1][0][0].data == "ccc"
    assert result[0][1][1][0].data == "ddd"
    assert result[0][1][1][1][0][0].data == "eee"
    assert result[0][1][1][1][1][0].data == "fff"


def test__lisp():
    data = "('aaa', ('bbb', ('ccc')), ('ddd', ('eee', 'fff')))"

    result = lisp(data)
    expected = [
        ["'aaa', ", ["'bbb', ", ["'ccc'"]], ", ", ["'ddd', ", ["'eee', 'fff'"]]]
    ]
    assert result == expected


def test__lisp_program():
    code = [
        "{\n",
        "    aaa\n",
        "    {\n",
        "        bbb\n",
        "        {\n",
        "            ccc\n",
        "        }\n",
        "    }\n",
        "    {\n",
        "        ddd\n",
        "        {\n",
        "            eee\n",
        "            fff\n",
        "        }\n",
        "    }\n",
        "}\n",
    ]
    code = "".join(code)

    result = lisp(code, char="{}")
    expected = [
        [
            "\n    aaa\n    ",
            ["\n        bbb\n        ", ["\n            ccc\n        "], "\n    "],
            "\n    ",
            [
                "\n        ddd\n        ",
                ["\n            eee\n            fff\n        "],
                "\n    ",
            ],
            "\n",
        ],
        "\n",
    ]
    assert result == expected


def to_tree(tree):
    result = []
    for a, _, c in tree:
        result.append([a, to_tree(c)])
    return result


def to_list(tree, indent=0):
    result = []
    for a, b, c in tree:
        result.append((indent, a))
        result.extend(to_list(c, indent + b))
    return result


strat_codeline = from_regex(r"\A[a-z]{3}\Z")


def f(strat):
    return lists(
        builds(list, tuples(strat_codeline, integers(min_value=1, max_value=8), strat))
    )


strat_nochildren = just([])
strat_children = recursive(strat_nochildren, f)


@given(strat_children)
def test_from_list(e):
    before = to_list(e)
    expected = to_tree(e)
    result = from_list(before, simple=True)
    assert result == expected


def add_brackets(tree, brackets=None):
    if brackets is None:
        brackets = ["{", "}"]

    result = [brackets[0]]
    for e in tree:
        if isinstance(e, str):
            result.append(e)
        else:
            result.append(add_brackets(e, brackets))

    result.append(brackets[1])
    return "".join(result)


def fuse_strings(tree):
    result = []
    for e in tree:
        if isinstance(e, str):
            result.append(e)
        else:
            result.append(fuse_strings(e))

    i = 0
    while i + 1 < len(result):
        if isinstance(result[i], str) and isinstance(result[i + 1], str):
            result[i] += result[i + 1]
            del result[i + 1]
        else:
            i += 1

    return result


@given(recursive(from_regex(r"\A[a-z]{3}\Z"), lists))
def test_lisp(e):
    before = add_brackets(e)
    expected = [fuse_strings(e)]

    result = lisp(before, "{}")
    assert result == expected
