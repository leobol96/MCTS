import math
import random

from node import Node
from tree import Tree


def ucb_selection(parent: Node, c: int) -> Node:
    left = parent.left
    right = parent.right

    if left.n_a == 0 and right.n_a == 0:
        return random.choice([left, right])
    elif left.n_a == 0 and right.n_a != 0:
        return left
    elif left.n_a != 0 and right.n_a == 0:
        return right

    ucb_left = left.t + c * math.sqrt(math.log(parent.n_a) / left.n_a)
    ucb_right = right.t + c * math.sqrt(math.log(parent.n_a) / right.n_a)

    if ucb_left > ucb_right:
        return left
    elif ucb_right > ucb_left:
        return right
    else:
        return random.choice([left, right])


if __name__ == '__main__':

    steps = 1000000
    c = 100
    tree = Tree(12)
    leaf_node = {}
    rewards = []

    for node in tree.total_node:
        if node.is_leaf():
            rewards.append(node.reward[0])

    for step in range(steps):
        if step % 10000 == 0:
            print('Step: ' + str(step))

        passed_node = [tree.root]
        current_node = tree.root
        while current_node.n_a != 0:
            # tree traversal
            current_node = ucb_selection(current_node, c)
            passed_node.append(current_node)
            if current_node.is_leaf():
                break

        # Expansion
        if not current_node.is_leaf():
            current_node = random.choice([current_node.left, current_node.right])
            passed_node.append(current_node)

        # Simulation
        while not current_node.is_leaf():
            current_node = random.choice([current_node.left, current_node.right])

        if current_node.reward[0] in leaf_node:
            leaf_node[(current_node.reward[0])] += 1
        else:
            leaf_node[(current_node.reward[0])] = 1

        # Back-up
        passed_node.reverse()
        for node in passed_node:
            node.n_a += 1
            node.t += current_node.reward[0]

    print('Found value :' + str(max(leaf_node, key=leaf_node.get)))
    print('Best value :' + str(max(rewards)))
