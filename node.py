class Node(object):
    """
    The Node class is used to build the binary tree.
    Each node that is not a leaf is connected to two children, the right one and the left one.
    """

    def __init__(self, t=0, n_a=0, reward=None, left=None, right=None):
        """
        Constructor method
        :param t: Reward got reaching this node
        :param n_a: Number of times reached this node
        :param reward: Reward given (only if the node is a leaf)
        :param left: Left child connected to the node
        :param right: Right child connected to the node
        """
        self.t = t
        self.n_a = n_a
        self.reward = reward
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        """
        The method is used to return if the node is a leaf or not.
        A node is a leaf only in the reward is not None.
        :return: True if the node is a leaf.
        """
        if self.reward is not None:
            return True
        return False

    def is_snowcamp_leaf(self) -> bool:
        """
        This method is used to return if the node is a lead node for the snowCamp
        :return: If the node is a tree for the snowcamp.
        """
        if self.n_a == 0:
            return True
        return False
