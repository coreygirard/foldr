import unittest
import doctest
import foldr

class Test(unittest.TestCase):
    def test_basic(self):
        data = [(0,'aaa'),
                (1,'bbb'),
                (2,'ccc'),
                (1,'ddd'),
                (2,'eee'),
                (2,'fff')]

        result = foldr.fromList(data,simple=True)
        expected = ['aaa',
                    [['bbb',
                     [['ccc', []]]],
                      ['ddd',
                      [['eee', []],
                       ['fff', []]]]]]

        self.assertEqual(result,expected)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(foldr))
    return tests

if __name__ == '__main__':
    unittest.main()
