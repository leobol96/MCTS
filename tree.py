import numpy as np

from node import Node


def numpy_pop(numpy_array):
    to_return = numpy_array[0]
    numpy_array = np.delete(numpy_array, 0)
    return numpy_array, [to_return]


class Tree(object):

    def __init__(self, height):
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
                    distribution, reward = numpy_pop(distribution)
                    new_level.append(Node(reward=reward))

            tmp = new_level[:]
            for node in old_level:
                node.left = tmp.pop()
                node.right = tmp.pop()
                self.total_node.append(node.left)
                self.total_node.append(node.right)
            old_level = new_level
