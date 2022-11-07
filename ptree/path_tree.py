from .node import Node

class PTree(object):
    _root = None

    def __init__(self, **kwargs):
        pass

    @property
    def root(self):
        return self._root

    def tree_print(self, **kwargs):
        self.root.tree_print()

    def to_df(self, **kwargs):
        self.root.to_df

    def add_sequence(self, queue):
        self.root.add_sequence(queue)
    
