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







data = [(0,'aaa'),
        (1,'bbb'),
        (2,'ccc'),
        (1,'ddd'),
        (2,'eee'),
        (2,'fff'),
        (0,'ggg'),
        (1,'hhh')]

#pprint(fromList(data,simple=True),width=1)







import re

# TODO: optimize
def lisp(line,char=None):
    if not char:
        start,finish = '(',')'
    else:
        start,finish = char

    line = list(line)

    assert(line.count(start) == line.count(finish))


    for n in range(1):
        last = None
        i = 0
        while True:
            if line[i] == start:
                last = i
            if line[i] == finish:
                break
            if i >= len(line):
                break
            i += 1

        if i >= len(line):
            break

        if last:
            before = line[:last]
            during = []
            for e in line[last+1:i]:

            after = line[i+1:]



    #line = re.sub(re.escape(start),r'[',line)
    #line = re.sub(re.escape(finish),r']',line)
    #return eval(line)
    return line



data = "('aaa', ('bbb', ('ccc')), ('ddd', ('eee', 'fff')))"
#data = "('aaa', ('bbb', (['ccc' for i in range(100)])), ('ddd', ('eee', 'fff')))"

pprint(lisp(data),width=1)


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
