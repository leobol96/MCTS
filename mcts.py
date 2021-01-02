import math
import random
import numpy as np

import common_functions
from node import Node
from tree import Tree


def ucb_selection(parent: Node, c: int) -> Node:
    """
    UCB algorithm. Given the parent it returns the child using UCB formula
    :param parent: Parent
    :param c: Constant C to use in the UCB formula
    :return: Child choosen
    """
    left = parent.left
    right = parent.right

    if left.n_a == 0 and right.n_a == 0:
        return random.choice([left, right])
    elif left.n_a == 0 and right.n_a != 0:
        return left
    elif left.n_a != 0 and right.n_a == 0:
        return right

    ucb_left = left.t / left.n_a + c * math.sqrt(math.log(parent.n_a) / left.n_a)
    ucb_right = right.t / right.n_a + c * math.sqrt(math.log(parent.n_a) / right.n_a)

    if ucb_left > ucb_right:
        return left
    elif ucb_right > ucb_left:
        return right
    else:
        return random.choice([left, right])


def max_child(parent: Node) -> Node:
    """
    This method is used to select the new root.
    The new root will be the one with the higher mean -> (t/n(a))
    :param parent: Parent node
    :return: Node with the higher mean
    """
    if parent.left.t / parent.left.n_a > parent.right.t / parent.right.n_a:
        return parent.left
    elif parent.left.t / parent.left.n_a < parent.right.t / parent.right.n_a:
        return parent.right
    else:
        return random.choice([parent.left, parent.right])


if __name__ == '__main__':

    c_list = np.arange(0, 1000, 1)
    n_iterations = 50
    n_rollout = 5
    height = 12
    n_time_same_c = 1
    rewards = []

    # Creation of a single tree for each c values
    tree = Tree(height)
    for node in tree.total_node:
        if node.is_leaf():
            rewards.append(node.reward[0])

    max_child_values = []
    for c_value in c_list:
        print('Computation for C: ' + str(c_value))

        for _ in range(n_time_same_c):
            # Make a copy of the root to don't forget it for the next c_value
            tree.initialize()
            root_copy = tree.root
            tmp_max_value = []

            # Until the end of the tree
            while not root_copy.is_leaf():
                # For each iteration
                for iteration in range(n_iterations):
                    passed_node = [root_copy]
                    current_node = root_copy

                    # Three policy
                    while not current_node.is_snowcamp_leaf() and not current_node.is_leaf():
                        current_node = ucb_selection(current_node, c_value)
                        passed_node.append(current_node)

                    # Three expansion
                    if not current_node.is_leaf():
                        current_node = random.choice([current_node.left, current_node.right])
                        passed_node.append(current_node)

                    # For a number of rollout
                    for rollout in range(n_rollout):
                        current_node_copy = current_node

                        # Roll-out
                        while not current_node_copy.is_leaf():
                            current_node_copy = random.choice([current_node_copy.left, current_node_copy.right])

                        # Back-up
                        passed_node.reverse()
                        for node in passed_node:
                            node.n_a += 1
                            node.t += current_node_copy.reward[0]

                #root_copy = ucb_selection(root_copy, c_value)
                root_copy = max_child(root_copy)

            tmp_max_value.append(root_copy.reward[0])
            root_copy = tree.root
        max_child_values.append(sum(tmp_max_value) / len(tmp_max_value))
    optimal_values = len(max_child_values) * [max(rewards)]

    common_functions.plot_char(height=str(height),
                               n_iterations=str(n_iterations),
                               n_rollout=str(n_rollout),
                               labels=c_list,
                               max_child_values=max_child_values,
                               optimal_values=optimal_values,
                               smooth=False)

    for sigma in range(1, 20, 1):
        common_functions.plot_char(height=str(height),
                                   n_iterations=str(n_iterations),
                                   n_rollout=str(n_rollout),
                                   labels=c_list,
                                   max_child_values=max_child_values,
                                   optimal_values=optimal_values,
                                   smooth=True,
                                   sigma=sigma)
