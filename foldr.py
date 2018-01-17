from pprint import pprint



class FoldrNode(object):
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



import ctypes
a = "hello world"
idA = id(a)
print(idA)
c = ctypes.cast(idA,ctypes.py_object)
print(c.value)
c.value = 7
print(c.value)

#print ctypes.cast(id(a), ctypes.py_object).value


class Example(object):
    def __init__(self, parent, i):
        self.parent = parent
        self.i = i

    def __setattr__(self,k,v):
        self.parent.set(k,v)

class Container(object):
    def __init__(self):
        self.vec = [1,2,3,4,5]

    def set(self,k,v):
        self.vec[k] = v

    def __iter__(self):
        for i in range(len(self.vec)):
            yield Example(self,i)



container = Container()
for i in container:
    print(i)



'''
def makeIterator(t):
    for i in range(len(t)):
        yield id(t[i])

lst = [1,2,3]

for ptr in makeIterator(lst):
    print(ptr)

print(lst)
'''





'''
for ptr in makeIterator(tree):
    temp = ptr
    temp += 1
    ptr = temp
'''


'''

Get iterator lists for each of depth-first and breadth-first search
through the tree:

for ptr in makeIterator(tree,mode='depth'):
    ptr = None

'''
