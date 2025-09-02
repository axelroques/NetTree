
import matplotlib.pyplot as plt
import numpy as np


def plot_patterns(
        data,
        series_labels,
        patterns,
        i_pattern,
        show_symbols=True
):
    """
    Colorify the dataset for visual interpretation of the patterns.
    """

    n_row = data.shape[0]
    n_col = data.shape[1]

    _, ax = plt.subplots(figsize=(12, 0.6*n_row))
    colors = ['#83a83b', '#c44e52', '#8172b2', '#ff914d', '#77BEDB']

    # Color the i_pattern^th pattern
    pattern = patterns[i_pattern]

    # Iterate over the individual node positions
    for node in pattern:
        x, y = node.pos
        ax.axhspan(
            ymin=-y+n_row, ymax=-y-1+n_row,
            xmin=x/n_col, xmax=(x+1)/n_col,
            facecolor=colors[y % len(colors)],
            alpha=0.8,
        )

    # Grid
    for i_row in range(n_row):
        for i_col in range(n_col):
            ax.axhspan(
                ymin=i_row, ymax=i_row+1,
                xmin=i_col/n_col, xmax=(i_col+1)/n_col,
                facecolor='none',
                edgecolor='silver',
                alpha=0.5
            )

            # Show symbols (optional)
            if show_symbols:
                ax.text(
                    x=(i_col+0.5)/n_col, y=1-(i_row+0.5)/n_row,
                    s=data[i_row, i_col], ha='center', va='center',
                    transform=ax.transAxes
                )

    # y axis parameters
    ax.set_title(f'Occurrence {i_pattern}')
    ax.set_xticklabels('')
    ax.set_yticks(np.arange(n_row) + 0.5)
    ax.set_yticklabels([l for l in series_labels][::-1])
    ax.grid(visible=False)
    ax.xaxis.set_visible(False)   

    plt.show()

    return
