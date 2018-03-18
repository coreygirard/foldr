
'''
class Example(object):
    def __init__(self):
        self.__dict__['vec'] = [1,2,3,4,5]
        self.__dict__['x'] = None

    def __iter__(self):
        for i in range(len(self.vec)):
            yield self.x

    def __setattr__(self,k,v):
        print(k,v)

class Ptr(object):
    def __init__(self):
        pass

    def __coerce__(self, other):
        print(self,other)

#ptr = Ptr()

#ptr + 3


example = Example()
example.x = 456

for e in example:
    e = 3
'''





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

    def __setattr__(self, k, v):
        self.parent.set(k, v)

class Container(object):
    def __init__(self):
        self.vec = [1, 2, 3, 4, 5]

    def set(self, k, v):
        self.vec[k] = v

    def __iter__(self):
        for i in range(len(self.vec)):
            yield Example(self, i)


'''
container = Container()
for i in container:
    print(i)
'''






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
