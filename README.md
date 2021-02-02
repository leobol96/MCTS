# MCTS
Monte carlo tree search

## Structure

To implement the Monte Carlo Tree Search, the object-oriented paradigm has been used. The data structure consists of the following classes:
	
 1) The **Node** class is the core part of a tree and it is structured as below.

    **Class variables**:

    - reward: it represents the reward that an agent gets if it reaches this node. Only leaves nodes have rewards.
    - t: it represents the total amount of rewards got from the previous MTCS iterations that passed from the node.
    - n_a : it represents the total number of times the node has been visited. 
    - left : it represents the left child of the node. It is an instance of the Node class.
    - right : it represents the right child of the node. It is an instance of the Node class. 

    **Class methods**:

    - is_leaf : this method returns True if the reward value is valorized (not None).
    - is_snowcamp_leaf: This method returns True if the n_a variable is equal to 0.


2) The **Tree** Class represents the binary tree where the MCTS is performed. This is built iteratively from level one to the maximum level of the tree. Each node of the old level is iterated, and a new instance of the node class is created for each left and right child. 
Levels have exactly 2^{level} nodes, so the last level has 2^{12} leaves. Leaves represent the end of the tree and are the only node with a valorized reward variable. These rewards are values taken from a uniform continuous distribution from 0 to 100.

    **Class variables**:

    - root : the root node of the tree
    - total_node:  it is a list that contains all the nodes part of the tree. 

    **Class methods**:
    - initialize: this method resets the variables n_a and t in each node of the tree. It is implemented to reuse the same tree without creating a new one.

<p align="center">
  <img width="460" height="300" src="/doc/images/tree.png">
</p>

## Results

During the Monte Carlo Tree search procedure, the next child is chosen randomly, and for this reason, the MCTS is not deterministic. The final reward can, in fact, vary despite of performing twice the same procedure with the same C parameter.

To overcome this problem, and to draw more reliable graphs, a trick was taken. For each value of c, from 1 to 1000, the MCTS algorithm has been executed more times (30). In order to avoid missing possible maximums on low c values and to decrease the computational time for high c values, the list of c values from 1 to 1000 has been created as follows:

-	0-1 step size of 0.1
-	1-10 step size of 0.5
-	10-100 step size of 1
-	100-1000 step size of 5   

Afterwards, the average for each score has been calculated, and it has been drawn in the graph below.

![Results](/doc/images/2109_02_01_2021.png)

The MAX and the ROBUST best child methods obtain by far the best results. Considering only these two methods, the average score tends to increase for low c parameter between 0 and 70. It reaches the optimal value at 100 and after 200 slowly begins to decrease. Hence, it is possible to state that the optimal c value is around 100 and 200, but one could also obtain good results using values around 70 and 300.

As a test, the UCB score was also used to choose the new root of the tree (UCB best child method). The green line represents the average score obtained from the UCB child selection. The results show how the curve is totally different from the others, and rapidly decreases while the c value increases. This occurs because the exploration factor in the UCB equation increases, and instead of choosing the most promising child, it is chosen the unexplored one.





## Installation
Open the terminal in the current folder and digit:

```sh 
pip install -r requirements.txt 
```

```sh 
python mcts.py
```
