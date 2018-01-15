from pprint import pprint

'''
Small script to make folding linear data formats into tree structures easy
'''


'''
One module that accepts data like this:

[(0,'aaa'),
 (1,'bbb'),
 (2,'ccc'),
 (1,'ddd'),
 (2,'eee'),
 (2,'fff')]

and folds it like this:

['aaa',
 [['bbb',
   [['ccc', []]]],
  ['ddd',
   [['eee', []],
    ['fff', []]]]]]

'''


class Node(object):
    def __init__(self,depth,code):
        self.depth = depth
        self.code = code
        self.parent = None
        self.children = []

    def add(self,child):
        child.parent = self
        self.children.append(child)


def simplify(head):
    resp = [head.code,[]]
    for e in head.children:
        resp[1].append(simplify(e))
    return resp

def fromList(lines,simple=False,member=None):
    '''
    >>> data = [(0,'aaa'),
    ...         (1,'bbb'),
    ...         (2,'ccc'),
    ...         (1,'ddd'),
    ...         (2,'eee'),
    ...         (2,'fff')]
    >>> r = fromList(data,simple=True)
    >>> r == ['aaa',
    ...       [['bbb',
    ...         [['ccc', []]]],
    ...        ['ddd',
    ...         [['eee', []],
    ...          ['fff', []]]]]]
    True
    '''

    root = Node(-4,'')
    ptr = root
    for e in lines:
        if member == None:
            depth,code = e
        else:
            depth = getattr(e,member)
            code = e

        line = Node(depth,code)

        if line.depth > ptr.depth:
            ptr.add(line)
            ptr = ptr.children[-1]
        elif line.depth == ptr.depth:
            ptr = ptr.parent
            ptr.add(line)
            ptr = ptr.children[-1]
        else:
            while line.depth < ptr.depth:
                ptr = ptr.parent
            ptr = ptr.parent
            ptr.add(line)
            ptr = ptr.children[-1]

    if simple:
        return simplify(root.children[0])
    else:
        return root.children[0]




data = [(0,'aaa'),
        (1,'bbb'),
        (2,'ccc'),
        (1,'ddd'),
        (2,'eee'),
        (2,'fff')]

#pprint(fromList(data,simple=True),width=1)







import re

def lisp(line,char=None):
    if not char:
        start,finish = '(',')'
    else:
        start,finish = char

    line = re.sub(re.escape(start),r'[',line)
    line = re.sub(re.escape(finish),r']',line)
    return eval(line)



data = "('aaa', ('bbb', ('ccc')), ('ddd', ('eee', 'fff')))"
#data = "('aaa', ('bbb', (['ccc' for i in range(100)])), ('ddd', ('eee', 'fff')))"

#pprint(lisp(data),width=1)


'''
Another module that accepts data like this:

('aaa', ('bbb', ('ccc')), ('ddd', ('eee', 'fff')))

and folds it

It can also handle:

{
    'aaa',
    {
        'bbb',
        {
            'ccc'
        }
    },
    {
        'ddd',
        {
            'eee',
            'fff'
        }
    }
}


'''


'''

Get iterator lists for each of depth-first and breadth-first search
through the tree:

for ptr in makeIterator(tree,mode='depth'):
    ptr = None

'''
