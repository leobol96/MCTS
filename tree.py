import numpy as np
from node import Node


class Tree(object):

    def __init__(self, height):
        # Build a three
        self.total_node = []
        self.root = Node()
        self.total_node.append(self.root)
        old_level = [self.root]
        for level in range(1, height+1):
            if level != height:
                # For all the nodes that are not leaves
                new_level = [Node() for count in range(2 ** level)]
            else:
                new_level = [Node(reward=np.random.normal(0, 100, 1)) for count in range(2 ** level)]
            tmp = new_level[:]
            for node in old_level:
                node.left = tmp.pop()
                node.right = tmp.pop()
                self.total_node.append(node.left)
                self.total_node.append(node.right)
            old_level = new_level
