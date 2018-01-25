import unittest
import doctest
import foldr
from pprint import pprint

class Test(unittest.TestCase):
    def test_basic(self):
        data = [(0,'aaa'),
                (1,'bbb'),
                (2,'ccc'),
                (1,'ddd'),
                (2,'eee'),
                (2,'fff')]

        result = foldr.fromList(data,simple=True)
        expected = [['aaa',
                     [['bbb',
                       [['ccc', []]]],
                      ['ddd',
                       [['eee', []],
                        ['fff', []]]]]]]

        self.assertEqual(result,expected)


        data = [(0,'aaa'),
                (1,'bbb'),
                (0,'ccc'),
                (1,'ddd')]

        result = foldr.fromList(data,simple=True)
        expected = [['aaa',
                     [['bbb',[]]]],
                    ['ccc',
                     [['ddd',[]]]]]

        self.assertEqual(result,expected)


class TestFromAttribute(unittest.TestCase):
    def test_from_attribute(self):
        class Example(object):
            def __init__(self,depth,data):
                self.depth = depth
                self.data = data

        data = [Example(0,'aaa'),
                Example(1,'bbb'),
                Example(2,'ccc'),
                Example(1,'ddd'),
                Example(2,'eee'),
                Example(2,'fff')]

        result = foldr.fromAttribute(data,'depth',simple=True)
        #pprint(result)
        self.assertEqual(len(result),1)

        self.assertEqual(result[0][0].data,'aaa')
        self.assertEqual(result[0][1][0][0].data,'bbb')
        self.assertEqual(result[0][1][0][1][0][0].data,'ccc')
        self.assertEqual(result[0][1][1][0].data,'ddd')
        self.assertEqual(result[0][1][1][1][0][0].data,'eee')
        self.assertEqual(result[0][1][1][1][1][0].data,'fff')

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
        self.assertEqual(result,expected)

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

        result = foldr.lisp(code,char='{}')
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
        self.assertEqual(result,expected)



def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(foldr))
    return tests

if __name__ == '__main__':
    unittest.main()
