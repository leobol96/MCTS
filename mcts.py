import math
import random
import common_functions
from statistics import median

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

    ucb_left = left.t/left.n_a + c * math.sqrt(math.log(parent.n_a) / left.n_a)
    ucb_right = right.t/right.n_a + c * math.sqrt(math.log(parent.n_a) / right.n_a)

    if ucb_left > ucb_right:
        return left
    elif ucb_right > ucb_left:
        return right
    else:
        return random.choice([left, right])


if __name__ == '__main__':

    found_values_c = []
    optimal_values_c = []
    c_list = [0.01, 0.1, 0.5, 1, 2, 5, 10, 50, 100, 1000]
    #c_list = [0.01, 0.1]
    n_iterarionts = 10

    for c_value in c_list:
        print('***********************************')
        print('Episodes for C values', str(c_value))
        tmp_found_values = []
        tmp_optimal_values = []
        for episode in range(n_iterarionts):
            print('Episode: ' + str(episode+1))
            steps = 100000
            c = c_value
            tree = Tree(12)
            leaf_node = {}
            rewards = []

            for node in tree.total_node:
                if node.is_leaf():
                    rewards.append(node.reward[0])

            for step in range(steps):
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
            print('-----------------------')
            tmp_found_values.append(max(leaf_node, key=leaf_node.get))
            tmp_optimal_values.append(max(rewards))
        found_values_c.append(round(sum(tmp_found_values) / len(tmp_found_values), 3))
        optimal_values_c.append(round(sum(tmp_optimal_values) / len(tmp_optimal_values), 3))
        #found_values_c.append(median(tmp_found_values))

    common_functions.plot_bar_char(labels=c_list, found_values=found_values_c, optimal_values=optimal_values_c)
