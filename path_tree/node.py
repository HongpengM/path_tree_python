from functools import reduce
from lib2to3.pgen2.pgen import DFAState
import pandas as pd

class Node(object):
    _path = ''
    _data = None
    _parent = None
    _children = []
    _path_func =None

    def __init__(self, data, **kwargs) -> None:
        self._data = data
        self._path =  (kwargs['path_func'])(data) if 'path_func' in kwargs else data
        self._path_func = kwargs['path_func'] if 'path_func' in kwargs else None
        self._parent = kwargs['parent'] if 'parent' in kwargs else None
        self._children = kwargs['children'] if 'children' in kwargs else []
        
    @property
    def path(self):
        return self._path
    @property
    def parent(self):
        return self._parent
    @property
    def children(self):
        return self._children
    @property
    def path_func(self):
        return self._path_func
    @property
    def data(self):
        return self._data
    @property
    def depth(self):
        if self.parent:
            return self.parent.depth + 1
        else:
            return 0
    @property
    def is_root(self):
        return self.parent == None
    @property
    def is_leaf(self):
        return len(self.children) == 0

    @parent.setter
    def parent(self, value):
        self._parent = value
        value._children.append(self)
    
    @children.setter
    def children(self, value):
        self._children = value
        value.parent = self

    @data.setter
    def data(self, value):
        self._data = value
        self._path = (self._path_func)(value) if self._path_func != None else value
    
    @path_func.setter
    def path_func(self, value):
        self._path_func = value

    def _to_list(self):
        if not self.is_leaf:
            children_lists = reduce(lambda a, b: a + b, 
                map(lambda x: x._to_list(), self._children))

            return list(map(lambda x: [self.path]  + x, 
                             children_lists))
        else:
            return  [[self.path]]
    
    def to_list(self,sep=''):
        return list(map(lambda x: '/'.join(x), 
                        list(self._to_list())))

    def _to_df(self):
        return pd.DataFrame(self._to_list())

    def to_df(self):
        return self._to_df().rename(columns=lambda x: 'depth ' + str(x) if x > 0 else 'root')

    def stats_df(self, **kwargs):
        _df = self.to_df().fillna('$')
        max_depth = _df.shape[1]
        if 'depth' in kwargs:
            if kwargs['depth']+1 < max_depth:
                return _df.groupby(by=list(_df.columns[0:kwargs['depth']+1])).count().rename(columns={_df.columns[kwargs['depth']+1]:'count'})
            else:
                _df['count'] = 1
                return _df