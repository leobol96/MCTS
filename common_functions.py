import matplotlib.pyplot as plt
import numpy as np


def plot_bar_char(height, n_episodes, n_steps, labels, robust_values, max_values, optimal_values):
    """
    Function to plot a bar char with bars per each label
    :param height: Height of the tree
    :param n_episodes: Number of episodes for each C
    :param n_steps: Number of steps for each episode
    :param max_values: Mean of the max children values
    :param labels: Label corresponding the C value
    :param robust_values:  Mean of the robust children values
    :param optimal_values: Mean of the best possible values
    """
    x = np.arange(len(labels))  # the label locations
    width = 0.30  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, robust_values, width, label='Robust child')
    rects2 = ax.bar(x, max_values, width, label='Max child')
    rects3 = ax.bar(x + width, optimal_values, width, label='Optimal child')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title(
        'Average of the scores obtained with depth: ' + height + ', episodes: ' + n_episodes + ' and ' + n_steps + ' steps for each episode')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    auto_label(rects1, ax)
    auto_label(rects2, ax)
    auto_label(rects3, ax)
    fig.tight_layout()
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
