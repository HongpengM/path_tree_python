'''
Description: 
Author: Kevin
Date: 2022-11-02 20:01:27
Github: no way to find
LastEditTime: 2022-11-02 20:11:49
'''
from .node import Node

def main():
    a = Node('test')
    b = Node('letter')
    c = Node('number')
    d = Node('plus')
    e = Node('minus')
    b.parent = a
    c.parent = b
    d.parent = c
    e.parent = c
    print('test')
    print(a.is_root)
    print(b.is_root)
    print(a.children)
    print(a.is_leaf)
    print(b.is_leaf)

    print(a.to_list())
    print(a.to_df())
    print(vars(a))
    print(a.stats_df(depth=2))
    #print(a.stats_df())
    

if __name__ == '__main__':
    main()
