from functools import reduce
from collections import namedtuple, deque
import pandas as pd
import uuid


class Style:
    vertical_pad = '|    '
    not_last = '|--- '
    void_pad = '     '
    last = '+--- '


class Node(object):
    _uuid = ''
    _path = ''
    _data = None
    _parent = None
    _children = []
    _path_func = None
    _style = Style()
    _meta = None

    def __init__(self, data=None, path_func=None, parent=None) -> None:
        """_summary_

        Args:
            data (_type_, optional): data structure. Defaults to None.
            path_func (_type_, optional): generate path from data. Defaults to None.
            parent (_type_, optional): parent node. Defaults to None.
        """        
        self._uuid = uuid.uuid4()
        self._data = data
        self._path_func = path_func if path_func else (lambda x: x)
        self._path = (self._path_func)(data) if not data == None else ''
        self._parent = parent if isinstance(parent, Node) else None
        self._children = []

    @property
    def uuid(self):
        """_summary_

        Returns:
           UUID4 : uuid type 
        """        
        return self._uuid

    @property
    def path(self):
        """_summary_

        Returns:
            str: return path string of the node
        """        
        return self._path

    @property
    def parent(self):
        """_summary_

        Returns:
            Node: parent node
        """        
        return self._parent

    @property
    def children(self):
        """_summary_

        Returns:
            list: list of children nodes
        """        
        return self._children

    @property
    def path_func(self):
        """_summary_

        Returns:
            function: a function return path string
        """        
        return self._path_func

    @property
    def data(self):
        """_summary_

        Returns:
            data: 
        """        
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

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, value):
        self._meta = value
        
    @parent.setter
    def parent(self, value):
        self._parent = value
        if self not in self._parent._children:
            value._children.append(self)

    @data.setter
    def data(self, value):
        self._data = value
        self._path = (
            self._path_func)(value) if self._path_func != None else value

    @path_func.setter
    def path_func(self, value):
        self._path_func = value if callable(value) else (lambda x: x)

    def add_sequence(self, seq):
        """Add data in sequence

        Args:
            seq (list(data)): a list of data from the current node to the leaf node
        """        
        queue = deque(seq) if not isinstance(seq, deque) else seq
        _parent = self
        while len(queue) > 0:
            seq_insert = queue.popleft()
            exist_child = list(
                filter(lambda x: self._path_func(seq_insert),
                       _parent.children))
            if len(exist_child) > 0:
                exist_child[0].add_sequence(queue)
            else:
                new_child = Node(seq_insert, path_func=_parent.path_func)
                _parent.add_children(new_child)
                new_child.add_sequence(queue)

    def add_children(self, *children):
        for c in children:
            self._children.append(c)
            c.parent = self

    def _to_list(self):
        """_summary_
        create a 2d list of leaf paths
        each leaf is a list of its nodes' paths

        for example, a leaf a -> b -> c -> d -> e -> f 
        will be [[a, b, c, d, e, f]]

        Returns:
            list: a two dimension list
        """        
        if not self.is_leaf:
            children_lists = reduce(
                lambda a, b: a + b, map(lambda x: x._to_list(),
                                        self._children))

            return list(map(lambda x: [self.path] + x, children_lists))
        else:
            return [[self.path]]

    def to_list(self, sep='/'):
        return list(map(lambda x: sep.join(x), list(self._to_list())))

    def _to_df(self):
        return pd.DataFrame(self._to_list())

    def to_df(self):
        return self._to_df().rename(
            columns=lambda x: 'depth ' + str(x) if x > 0 else 'root')

    def stats_df(self, **kwargs):
        _df = self.to_df().fillna('$')
        max_depth = _df.shape[1]
        if 'depth' in kwargs:
            if kwargs['depth'] + 1 < max_depth:
                return _df.groupby(by=list(
                    _df.columns[0:kwargs['depth'] + 1])).count().rename(
                        columns={_df.columns[kwargs['depth'] + 1]: 'count'})
            else:
                _df['count'] = 1
                return _df

    def _tree_print(self,
                    root_style='',
                    children_pad='',
                    level=0,
                    maxlevel=False,
                    text_func=(lambda x: x.path)):
        """_summary_

        Args:
            root_style (str, optional): the padding for the first root Defaults to ''.
            children_pad (str, optional): children padding for the first root Defaults to ''.
            level (int, optional): to track max depth. Defaults to 0.
            maxlevel (bool, optional): limit max depth to this number. Defaults to False.
            text_func (tuple, optional): function(Node->str) return the representation string of the node. Defaults to (lambda x: x.path).

        Returns:
            list(str): string lines of the tree print
        """        
        _ = [''.join([root_style, text_func(self)])]
        for child in self.children:
            if (not maxlevel or level < maxlevel):
                if child._uuid == self.children[-1]._uuid:
                    _ += child._tree_print(
                        root_style=children_pad + self._style.last,
                        children_pad=children_pad + self._style.void_pad,
                        level=level + 1,
                        maxlevel=maxlevel,
                        text_func=text_func)
                else:
                    _ += child._tree_print(
                        root_style=children_pad + self._style.not_last,
                        children_pad=children_pad + self._style.vertical_pad,
                        level=level + 1,
                        maxlevel=maxlevel,
                        text_func=text_func)
        return _

    def tree_print(self, **kwargs):
        """
        print tree structure in console text
        """        
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