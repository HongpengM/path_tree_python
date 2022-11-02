'''
Description: 
Author: Kevin
Date: 2022-11-02 20:04:32
Github: no way to find
LastEditTime: 2022-11-02 23:44:49
'''
import unittest
from path_tree.node import Node

class TestNode(unittest.TestCase):

    def test_instance(self):
        n = Node('')
        self.assertIsInstance(n, Node)


if __name__ == '__main__':
    unittest.main()
    