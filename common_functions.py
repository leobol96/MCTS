import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d


def plot_bar_char(height, n_episodes, n_steps, labels, max_values, optimal_values):
    """
    Function to plot a bar char with bars per each label
    :param height: Height of the tree
    :param n_episodes: Number of episodes for each C
    :param n_steps: Number of steps for each episode
    :param max_values: Mean of the max children values
    :param labels: Label corresponding the C value
    :param optimal_values: Mean of the best possible values
    """
    x = np.arange(len(labels))  # the label locations
    width = 0.30  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, max_values, width, label='Max child')
    rects2 = ax.bar(x + width, optimal_values, width, label='Optimal child')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title(
        'Average of the scores obtained with depth: ' + height + ', episodes: ' + n_episodes + ' and ' + n_steps + ' steps for each episode')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    auto_label(rects1, ax)
    auto_label(rects2, ax)
    fig.tight_layout()
    plt.show()


def plot_char(height, n_iterations, n_rollout, labels_c, scores_list, labels_best_child, sigma: int = 2):
    """
    Plot a normal graph. The x-axis represents the C-values and the y-axis represents the mean of the scores for
    the robust child, the max child and the optimal child.
    :param height: Height of the tree
    :param n_iterations: Number of iterations
    :param n_rollout: Number of rollout steps
    :param labels_c: Labels of the c value
    :param scores_list: List of the scores. One list for every Best child method
    :param labels_best_child: Labels of the best child methods used
    :param sigma: Sigma to use to smooth the graph
    :return:
    """

    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    axs[0].set_title('Not smoothed')

    for idx, best_child_type in enumerate(scores_list):
        axs[0].plot(labels_c, best_child_type, label=labels_best_child[idx])
    axs[0].set_ylabel('Scores')
    axs[0].set_xlabel('C')
    axs[0].legend()

    axs[1].set_title('Smoothed with Sigma = ' + str(sigma))
    for idx, best_child_type in enumerate(scores_list):
        axs[1].plot(labels_c, gaussian_filter1d(best_child_type, sigma=sigma), label=labels_best_child[idx])
    axs[1].set_ylabel('Scores')
    axs[1].set_xlabel('C')
    axs[1].legend()

    fig.suptitle(
        'Average of the scores obtained with depth: ' + height + ', iterations: ' + n_iterations + ' and ' + n_rollout + ' rollouts for each iteration',
        fontsize=16)
    plt.show()


def auto_label(rects, ax):
    """
    Attach a text label above each bar in *rects*, displaying its height.
    :param rects: bar where attach the label
    :param ax: subplot
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def numpy_pop(numpy_array):
    """
    This method is the same of list.pop() but implemented for a numpy array
    :param numpy_array: numpy array from which delete the last element
    :return: From this function are returned two elements.
        - A copy of the same array without the element removed
        - The element removed
    """
    to_return = numpy_array[0]
    numpy_array = np.delete(numpy_array, 0)
    return numpy_array, [to_return]
