'''
Description: 
Author: Kevin
Date: 2022-11-02 20:04:32
Github: no way to find
LastEditTime: 2022-11-06 20:18:49
'''
import unittest
from path_tree.node import Node

class TestNode(unittest.TestCase):

    def test_null_instance(self):
        n = Node()
        self.assertIsInstance(n, Node)

    def test_empty_string_instance(self):
        n = Node('')
        self.assertIsInstance(n, Node)

    def test_list_instance(self):
        n = Node('www.test.org/test/index.html')
        self.assertEqual()

    def test_

if __name__ == '__main__':
    unittest.main()
    