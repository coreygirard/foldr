from pprint import pprint



class FoldrNode(object):
    def __init__(self,depth,code):
        '''
        >>> node = FoldrNode(0,'aaa')
        >>> node.add(FoldrNode(1,'bbb'))
        >>> node.add(FoldrNode(2,'ccc'))

        >>> node.depth
        0

        >>> node.code
        'aaa'

        >>> node.parent
        '''

        self.depth = depth
        self.code = code
        self.parent = None
        self.children = []

    def add(self,child):
        '''
        >>> node1 = FoldrNode(0,'aaa')
        >>> node2 = FoldrNode(1,'bbb')
        >>> node1.add(node2)

        >>> node1.children[0] == node2
        True
        >>> node2.parent == node1
        True
        '''

        child.parent = self
        self.children.append(child)


def simplify(head):
    '''
    >>> head = FoldrNode(0,'aaa')
    >>> head.add(FoldrNode(1,'bbb'))
    >>> head.add(FoldrNode(2,'ccc'))

    >>> simplify(head)
    ['aaa', [['bbb', []], ['ccc', []]]]
    '''

    resp = [head.code,[]]
    for e in head.children:
        resp[1].append(simplify(e))
    return resp

def fromList(lines,simple=False):
    '''
    >>> data = [(0,'aaa'),
    ...         (1,'bbb'),
    ...         (2,'ccc'),
    ...         (1,'ddd'),
    ...         (2,'eee'),
    ...         (2,'fff')]
    >>> r = fromList(data,simple=True)
    >>> r == [['aaa',
    ...        [['bbb',
    ...          [['ccc', []]]],
    ...         ['ddd',
    ...          [['eee', []],
    ...           ['fff', []]]]]]]
    True
    '''

    root = FoldrNode(-4,'')
    ptr = root
    for e in lines:
        depth,code = e

        line = FoldrNode(depth,code)

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
        return [simplify(c) for c in root.children]
    else:
        return [c for c in root.children]


def fromAttribute(lines,attr,simple=False):
    data = []
    for e in lines:
        try:
            data.append((getattr(e,attr),e))
        except:
            # TODO: anything
            pass

    return fromList(data,simple)

def fromMethod(lines,attr,simple=False):
    data = []
    for e in lines:
        try:
            data.append((getattr(e,attr)(),e))
        except:
            # TODO: anything
            pass

    return fromList(data,simple)



def collapseChars(s):
    during = [s.pop(0)]
    while len(s) > 0:
        if type(during[-1]) == type('string') and type(s[0]) == type('string'):
            during[-1] += s.pop(0)
        else:
            during.append(s.pop(0))
    return during


# TODO: optimize
def lisp(line,char=None):
    if not char:
        start,finish = '(',')'
    else:
        start,finish = char

    line = list(line)

    assert(line.count(start) == line.count(finish))


    while start in line:
        last = None
        i = 0
        while True:
            if i >= len(line):
                break
            if line[i] == start:
                last = i
            if line[i] == finish:
                break
            i += 1

        if i >= len(line):
            break

        if last != None:
            before = line[:last]
            during = collapseChars(line[last+1:i])

            after = line[i+1:]
            line = before+[during]+after

    return collapseChars(line)







'''
from pprint import pprint

tree = [(0,1),
        (1,2),
        (2,3),
        (2,4),
        (1,5),
        (2,6),
        (2,7)]

tree = fromList(tree,simple=True)

pprint(tree, width=20)
'''

'''
for i,ptr in enumerate(makeIterator(tree, type='in-order')):
    ptr = i
'''

'''
import ctypes


a = "hello world"
aPtr = id(a)
print(aPtr)
c = ctypes.cast(aPtr,ctypes.py_object)
print(c.value)
c.value = 7
print(c.value)
'''

'''
Get iterator lists for each of depth-first and breadth-first search
through the tree:

for ptr in makeIterator(tree,mode='depth'):
    ptr = None

'''
