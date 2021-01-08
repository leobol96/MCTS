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


def best_child(parent: Node, type_of_child: str) -> Node:
    """
    This method is used to select the new root.
    The new root will be the one with the higher mean (max) or the one with the max number of occurrences.
    :param type_of_child: max or robust. The default method will be the robust one.
    :param parent: Parent node
    :return: Best child
    """
    if type_of_child == 'max':
        if parent.left.t / parent.left.n_a > parent.right.t / parent.right.n_a:
            return parent.left
        elif parent.left.t / parent.left.n_a < parent.right.t / parent.right.n_a:
            return parent.right
        else:
            return random.choice([parent.left, parent.right])
    elif type_of_child == 'ucb':
        return ucb_selection(parent=parent, c=c_value)
    else:
        if parent.left.n_a > parent.right.n_a:
            return parent.left
        elif parent.left.n_a < parent.right.n_a:
            return parent.right
        else:
            return random.choice([parent.left, parent.right])


def mcts_steps(root):
    """
    This method implements the four basic steps of the MCTS.
        -   Selection
        -   Expansion
        -   Rollout
        -   Backup
    Given the root of the tree it will update the t and n(a) for each node visited in the procedure.
    :param root: Node from which to start searching
    """
    nodes_to_update = [root]
    current_node = root

    # Three policy
    while not current_node.is_snowcamp_leaf() and not current_node.is_leaf():
        current_node = ucb_selection(current_node, c_value)
        nodes_to_update.append(current_node)

    # Three expansion
    if not current_node.is_leaf():
        current_node = random.choice([current_node.left, current_node.right])
        nodes_to_update.append(current_node)

    # For a number of rollout
    for rollout in range(n_rollout):
        current_node_copy = current_node

        # Roll-out
        while not current_node_copy.is_leaf():
            current_node_copy = random.choice([current_node_copy.left, current_node_copy.right])

        # Back-up
        nodes_to_update.reverse()
        for node in nodes_to_update:
            node.n_a += 1
            node.t += current_node_copy.reward[0]


def print_scores(array_of_scores, limit_value):
    """
    This method print all the rewards and the c values used to obtain them.
    :param array_of_scores: Array of scores where check
    :param limit_value: Value limit. All the values above this limit will be printed.
    """
    for idx, x in enumerate(array_of_scores):
        if x > limit_value:
            print('Reward of: ' + str(x) + ' C: ' + str(c_list[idx]))


if __name__ == '__main__':

    # Create the c parameter list
    c_list = np.append(np.arange(0, 1, 0.1), np.arange(1, 10, 0.5), )
    c_list = np.append(c_list, np.arange(10, 150, 1))
    c_list = np.append(c_list, np.arange(100, 1000, 5))

    n_iterations = 50
    n_rollout = 5
    height = 12
    n_time_same_c = 30
    rewards = []
    best_child_methods = ['max', 'robust', 'ucb']
    # This list contains the rewards obtained with the combination of (C, best child method)
    scores = []

    # Creation of a single tree for each c values
    tree = Tree(height)
    # Create a list containing the rewards to calculate the maximum one
    for node in tree.total_node:
        if node.is_leaf():
            rewards.append(node.reward[0])

    # For every type of best child
    for type_child in best_child_methods:
        # For every type of C
        best_child_scores = []
        for c_value in c_list:
            print('Computation for C: ' + str(c_value) + ' and ' + type_child + ' best child')
            tmp_values = []
            # For n times for the same C
            for _ in range(n_time_same_c):
                # Make a copy of the root to don't forget it for the next c_value
                tree.initialize()
                root_copy = tree.root

                # Until the end of the tree
                while not root_copy.is_leaf():
                    # For each iteration
                    for iteration in range(n_iterations):
                        # Selection - Expansion - Simulation - Rollout
                        mcts_steps(root_copy)
                    # Choose the new root of the tree
                    root_copy = best_child(parent=root_copy, type_of_child=type_child)
                # Append the reward reached
                tmp_values.append(root_copy.reward[0])
                # Reset the root
                root_copy = tree.root
            # Append the mean of the values obtained using the same c value
            best_child_scores.append(sum(tmp_values) / len(tmp_values))
            # best_child_scores.append(max(tmp_values))
        # Append the reward obtained using a specific best child function
        scores.append(best_child_scores)

    # Add the optimal score to the scores list
    best_child_methods.append('optimal')
    scores.append(len(scores[0]) * [max(rewards)])

    # print_scores(np.array(scores[0]), 99.8)
    common_functions.plot_char(height=str(height),
                               n_iterations=str(n_iterations),
                               n_rollout=str(n_rollout),
                               labels_c=c_list,
                               scores_list=scores,
                               labels_best_child=best_child_methods,
                               sigma=4)
