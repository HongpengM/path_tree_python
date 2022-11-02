'''
Description: 
Author: Kevin
Date: 2022-11-02 20:01:27
Github: no way to find
LastEditTime: 2022-11-02 23:44:28
'''
from functools import reduce
from collections import namedtuple
import pandas as pd
import uuid
class Style:
   vertical_pad = '|   '
   not_last = '|-- '
   void_pad = '    '
   last = '+-- '
   

class Node(object):
    _uuid = ''
    _path = ''
    _data = None
    _parent = None
    _children = []
    _path_func =None
    _style=Style()

    def __init__(self, data, **kwargs) -> None:
        self._uuid = uuid.uuid4()
        self._data = data
        self._path =  (kwargs['path_func'])(data) if 'path_func' in kwargs else data
        self._path_func = kwargs['path_func'] if 'path_func' in kwargs else None
        self._parent = kwargs['parent'] if 'parent' in kwargs else None
        self._children = kwargs['children'] if 'children' in kwargs else []
    
    @property
    def uuid(self):
        return self._uuid
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
    def style(self):
        return self._style
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
        if self not in self._parent._children:
            value._children.append(self)

    @data.setter
    def data(self, value):
        self._data = value
        self._path = (self._path_func)(value) if self._path_func != None else value
    
    @path_func.setter
    def path_func(self, value):
        self._path_func = value

    def add_children(self, *children):
        for c in children:
            self._children.append(c)
            c.parent = self

    def _to_list(self):
        if not self.is_leaf:
            children_lists = reduce(lambda a, b: a + b, 
                map(lambda x: x._to_list(), self._children))

            return list(map(lambda x: [self.path]  + x, 
                             children_lists))
        else:
            return  [[self.path]]
    
    def to_list(self,sep='/'):
        return list(map(lambda x: sep.join(x), 
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

    def _tree_print(self, root_style='', children_pad='', level=0, maxlevel=False, text_func=(lambda x:x.path)):
        _  = [''.join([root_style, text_func(self)])]
        for child in self.children:
            if (not maxlevel or level < maxlevel):
                if child._uuid == self.children[-1]._uuid:
                    _ += child._tree_print(root_style=children_pad+self._style.last,
                                        children_pad=children_pad+self._style.void_pad,
                                        level = level+1,
                                        maxlevel = maxlevel,
                                        text_func=text_func)
                else:
                    _ += child._tree_print(root_style=children_pad+self._style.not_last,
                                        children_pad=children_pad+self._style.vertical_pad,
                                        level = level+1,
                                        maxlevel = maxlevel,
                                        text_func=text_func)
        return _
        
    def tree_print(self, **kwargs):
        print('\n'.join(self._tree_print(**kwargs)))


''' TODO Generator
def last_iterator_wrapper(iterable):
    
    # Returns iter, True for last one
    # else return iter, False for other positions
    
    iter_ = iter(iterable)
    try:
        item = next(iter_)
    except StopIteration:
        pass
    else:
        try:
            nextitem = next(iter_)
        except StopIteration:
            yield item, True
        else:
            yield item, False
            while True:
                _ = nextitem
                try: 
                    item = _
                    nextitem = next(iter_)
                except StopIteration:
                    yield item, True
                    break
                else:
                    yield item, False
'''