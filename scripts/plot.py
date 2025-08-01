import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_stack_height_analysis(stkhgt_data, save_dir="../plots", filename="stack_height_analysis.png"):
    """
    Create detailed plots and statistics for stack height data analysis.
    
    Parameters
    ----------
    stkhgt_data : pandas.Series
        Series containing stack height measurements in meters
    save_dir : str, optional
        Directory to save the plot file (default: "../plots")
    filename : str, optional
        Name of the output plot file (default: "stack_height_analysis.png")
        
    Returns
    -------
    None
        Displays plots and prints statistics
    """
    plt.style.use('classic')
    # Create bins for stack height categories
    categories = pd.cut(stkhgt_data, 
                       bins=[0, 10, 100, float('inf')],
                       labels=['0-10', '10-100', '>100'])

    # Create subplots - now 3 rows, 2 columns
    fig = plt.figure(figsize=(15, 18))
    gs = fig.add_gridspec(3, 2)

    # Distribution plot taking full width of top row
    ax_dist = fig.add_subplot(gs[0, :])
    # Modified to use bins with increment of 10
    max_height = int(stkhgt_data.max() // 10 * 10 + 10)  # Round up to nearest 10
    bins = range(0, max_height + 10, 10)  # Create bins from 0 to max in steps of 10
    sns.histplot(data=stkhgt_data, ax=ax_dist, bins=bins)
    ax_dist.set_title('Distribution of All Stack Heights')
    ax_dist.set_xlabel('Stack Height (m)')
    ax_dist.set_ylabel('Count')
    ax_dist.grid(True, alpha=0.3)

    # Box plots in bottom two rows
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])
    ax3 = fig.add_subplot(gs[2, 0])
    ax4 = fig.add_subplot(gs[2, 1])

    # Helper function to add stats text
    def add_stats(ax, data, x_pos=.6):
        stats = data.describe()
        stats_text = (
            f"Max: {stats['max']:.1f}m\n"
            f"Min: {stats['min']:.1f}m\n"
            f"Mean: {stats['mean']:.1f}m\n"
            f"Median: {stats['50%']:.1f}m\n"
            f"25%: {stats['25%']:.1f}m\n"
            f"75%: {stats['75%']:.1f}m\n"
            f"Std: {stats['std']:.1f}m"
        )
        ax.text(x_pos, 0.95, stats_text,
                transform=ax.transAxes,
                verticalalignment='top',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # Plot 1: All data
    bp1 = ax1.boxplot(stkhgt_data, tick_labels=['All Data'])
    ax1.set_title('All Stack Heights')
    ax1.set_ylabel('Stack Height (m)')
    ax1.grid(True, alpha=0.3)
    max_height_all = stkhgt_data.max()
    yticks_all = range(0, int(max_height_all) + 50, 50)
    ax1.set_yticks(yticks_all)
    add_stats(ax1, stkhgt_data)

    # Plot 2: 0-10 range
    data_0_10 = stkhgt_data[categories == '0-10']
    bp2 = ax2.boxplot(data_0_10, tick_labels=['0-10m'])
    ax2.set_title('Stack Heights 0-10m')
    ax2.set_ylabel('Stack Height (m)')
    ax2.grid(True, alpha=0.3)
    add_stats(ax2, data_0_10)

    # Plot 3: 10-100 range
    data_10_100 = stkhgt_data[categories == '10-100']
    bp3 = ax3.boxplot(data_10_100, tick_labels=['10-100m'])
    ax3.set_title('Stack Heights 10-100m')
    ax3.set_ylabel('Stack Height (m)')
    ax3.grid(True, alpha=0.3)
    add_stats(ax3, data_10_100)

    # Plot 4: >100 range with 50-step ticks
    data_100plus = stkhgt_data[categories == '>100']
    bp4 = ax4.boxplot(data_100plus, tick_labels=['>100m'])
    ax4.set_title('Stack Heights >100m')
    ax4.set_ylabel('Stack Height (m)')
    ax4.grid(True, alpha=0.3)
    max_height_100plus = data_100plus.max()
    yticks = range(100, int(max_height_100plus) + 50, 50)
    ax4.set_yticks(yticks)
    add_stats(ax4, data_100plus)

    plt.suptitle('', fontsize=16, y=0.95)
    plt.tight_layout()
    
    # Create save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Save the plot
    save_path = os.path.join(save_dir, filename)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()

    # Print summary statistics for each category
    print("\nSummary statistics by category:")
    print("\nAll data:")
    print(stkhgt_data.describe())
    for category in ['0-10', '10-100', '>100']:
        print(f"\nCategory {category}:")
        print(stkhgt_data[categories == category].describe())
