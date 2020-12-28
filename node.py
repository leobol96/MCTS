class Node(object):

    def __init__(self, t=0, n_a=0, reward=None,  left=None, right=None):
        self.t = t
        self.n_a = n_a
        self.reward = reward
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        if self.reward is not None:
            return True

