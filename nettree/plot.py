
import matplotlib.pyplot as plt
import numpy as np


def plot_patterns(
        data,
        patterns,
        i_pattern,
        show_symbols=True
):
    """
    Colorify the toy dataset for visual interpretation of the patterns.
    """

    n_row = data.shape[0]
    n_col = data.shape[1]

    _, ax = plt.subplots(figsize=(15, 0.5*n_row))
    colors = ['#911b58', '#6da7de', '#7db27a', '#ffcb77', '#eb8a90', '#e07be0']

    # Color the i_pattern^th pattern
    pattern = patterns[i_pattern]
    color = colors[i_pattern % len(colors)]

    # Iterate over the individual node positions
    for node in pattern:
        pos = node.pos
        ax.axhspan(
            ymin=-pos[0]+n_row, ymax=-pos[0]-1+n_row,
            xmin=pos[1]/n_col, xmax=(pos[1]+1)/n_col,
            facecolor=color,
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
    ax.set_yticklabels([f'S_{i}' for i in range(n_row)][::-1])
    ax.grid(visible=False)

    plt.show()

    return
