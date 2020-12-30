import matplotlib.pyplot as plt
import numpy as np


def plot_bar_char(labels, robust_values, max_values, optimal_values):
    """
    Function to plot a bar char with bars per each label
    :param labels: Label corresponding the C value
    :param robust_values: Value found with the algorithm
    :param optimal_values: Best possible value
    """
    x = np.arange(len(labels))  # the label locations
    width = 0.30  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, robust_values, width, label='Robust child')
    rects2 = ax.bar(x, max_values, width, label='Max child')
    rects3 = ax.bar(x + width, optimal_values, width, label='Optimal child')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores for each different C value')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    auto_label(rects1, ax)
    auto_label(rects2, ax)
    auto_label(rects3, ax)
    fig.tight_layout()
    plt.show()


def auto_label(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
