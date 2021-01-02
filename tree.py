import numpy as np
import common_functions

from node import Node


class Tree(object):
    """
    This class represents the Binary tree used to perform the MCTS algorithm.
    The tree is binary, so every node has two children the left one and the right one.
    """

    def __init__(self, height):
        """
        This is the constructor method of the tree.
        From the root, layer to layer, it builds the tree iteratively.
        The last layer of the tree will have 2^height leaves nodes.
        :param height: The height of the tree.
        """
        # Build a three
        self.total_node = []
        self.root = Node()
        self.total_node.append(self.root)
        old_level = [self.root]

        for level in range(1, height + 1):
            # For each level of the three
            if level != height:
                # For all the nodes that are not leaves
                new_level = [Node() for count in range(2 ** level)]
            else:
                # For all nodes that are leaves
                distribution = np.random.uniform(0, 100, 2 ** level)
                new_level = []
                for count in range(2 ** level):
                    distribution, reward = common_functions.numpy_pop(distribution)
                    new_level.append(Node(reward=reward))

            tmp = new_level[:]
            for node in old_level:
                node.left = tmp.pop()
                node.right = tmp.pop()
                self.total_node.append(node.left)
                self.total_node.append(node.right)
            old_level = new_level

    def initialize(self):
        """
        This function is used to initialize or reset the tree.
        This will set for each node of the tree the values t and n_a to 0.
        """
        for node in self.total_node:
            node.n_a = 0
            node.t = 0
