'''
Description: 
Author: Kevin
Date: 2022-11-02 20:01:27
Github: no way to find
LastEditTime: 2022-11-07 09:13:34
'''
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
    
