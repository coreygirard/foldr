import unittest
import doctest

from hypothesis import given
from hypothesis.strategies import recursive, lists, from_regex, just, tuples, builds, integers

import foldr2 as foldr


class Test(unittest.TestCase):
    def test_basic(self):
        data = [(0, 'aaa'),
                (1, 'bbb'),
                (2, 'ccc'),
                (1, 'ddd'),
                (2, 'eee'),
                (2, 'fff')]

        result = foldr.from_list(data, simple=True)
        expected = [['aaa',
                     [['bbb',
                       [['ccc', []]]],
                      ['ddd',
                       [['eee', []],
                        ['fff', []]]]]]]

        self.assertEqual(result, expected)


        data = [(0, 'aaa'),
                (1, 'bbb'),
                (0, 'ccc'),
                (1, 'ddd')]

        result = foldr.from_list(data, simple=True)
        expected = [['aaa',
                     [['bbb', []]]],
                    ['ccc',
                     [['ddd', []]]]]

        self.assertEqual(result, expected)


class TestFromAttribute(unittest.TestCase):
    def test_from_attribute(self):
        class Example(object):
            def __init__(self, depth, data):
                self.depth = depth
                self.data = data

        data = [Example(0, 'aaa'),
                Example(1, 'bbb'),
                Example(2, 'ccc'),
                Example(1, 'ddd'),
                Example(2, 'eee'),
                Example(2, 'fff')]

        result = foldr.from_attribute(data, 'depth', simple=True)
        #pprint(result)
        self.assertEqual(len(result), 1)

        self.assertEqual(result[0][0].data, 'aaa')
        self.assertEqual(result[0][1][0][0].data, 'bbb')
        self.assertEqual(result[0][1][0][1][0][0].data, 'ccc')
        self.assertEqual(result[0][1][1][0].data, 'ddd')
        self.assertEqual(result[0][1][1][1][0][0].data, 'eee')
        self.assertEqual(result[0][1][1][1][1][0].data, 'fff')

class TestLisp(unittest.TestCase):
    def test_lisp(self):
        data = "('aaa', ('bbb', ('ccc')), ('ddd', ('eee', 'fff')))"

        result = foldr.lisp(data)
        expected = [["'aaa', ",
                     ["'bbb', ",
                      ["'ccc'"]],
                     ", ",
                     ["'ddd', ",
                      ["'eee', 'fff'"]]]]
        self.assertEqual(result, expected)

class TestLispProgram(unittest.TestCase):
    def test_lisp_program(self):
        code = ["{\n",
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
                "}\n"]
        code = ''.join(code)

        result = foldr.lisp(code, char='{}')
        #pprint(result)
        expected = [["\n    aaa\n    ",
                     ["\n        bbb\n        ",
                      ["\n            ccc\n        "],
                      "\n    "],
                     "\n    ",
                     ["\n        ddd\n        ",
                      ["\n            eee\n            fff\n        "],
                      "\n    "],
                     "\n"],
                    "\n"]
        self.assertEqual(result, expected)


def to_tree(tree):
    result = []
    for a, _, c in tree:
        result.append([a, to_tree(c)])
    return result

def to_list(tree, indent=0):
    result = []
    for a, b, c in tree:
        result.append((indent, a))
        result.extend(to_list(c, indent+b))
    return result

strat_codeline = from_regex(r'\A[a-z]{3}\Z')

def f(strat):
    return lists(builds(list, tuples(strat_codeline, integers(min_value=1, max_value=8), strat)))

strat_nochildren = just([])
strat_children = recursive(strat_nochildren, f)
class TestFromList(unittest.TestCase):
    @given(strat_children)
    def test_from_list(self, e):
        before = to_list(e)
        expected = to_tree(e)
        result = foldr.from_list(before, simple=True)
        self.assertEqual(result, expected)





def add_brackets(tree, brackets=None):
    if brackets is None:
        brackets = ['{', '}']

    result = [brackets[0]]
    for e in tree:
        if isinstance(e, str):
            result.append(e)
        else:
            result.append(add_brackets(e, brackets))

    result.append(brackets[1])
    return ''.join(result)

def fuse_strings(tree):
    result = []
    for e in tree:
        if isinstance(e, str):
            result.append(e)
        else:
            result.append(fuse_strings(e))

    i = 0
    while i+1 < len(result):
        if isinstance(result[i], str) and isinstance(result[i+1], str):
            result[i] += result[i+1]
            del result[i+1]
        else:
            i += 1

    return result


class TestLispHypothesis(unittest.TestCase):
    @given(recursive(from_regex(r'\A[a-z]{3}\Z'), lists))
    def test_lisp(self, e):
        before = add_brackets(e)
        expected = [fuse_strings(e)]

        result = foldr.lisp(before, '{}')
        self.assertEqual(result, expected)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(foldr))
    return tests

if __name__ == '__main__':
    unittest.main()
