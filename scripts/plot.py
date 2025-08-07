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


def plot_stack_height_by_capacity(stkhgt_data, design_capacity_data, design_capacity_units_data, 
                                 target_unit="MW", save_dir="../plots", filename="stack_height_by_capacity.png"):
    """
    Create detailed plots and statistics for stack height analysis binned by design capacity.
    
    Parameters
    ----------
    stkhgt_data : pandas.Series
        Series containing stack height measurements in meters
    design_capacity_data : pandas.Series
        Series containing design capacity values
    design_capacity_units_data : pandas.Series
        Series containing design capacity units
    target_unit : str, optional
        Unit to filter for (default: "MW")
    save_dir : str, optional
        Directory to save the plot file (default: "../plots")
    filename : str, optional
        Name of the output plot file (default: "stack_height_by_capacity.png")
        
    Returns
    -------
    pandas.DataFrame
        DataFrame with filtered data and capacity categories
    """
    plt.style.use('classic')
    
    # Create a DataFrame with the three series
    df = pd.DataFrame({
        'stkhgt': stkhgt_data,
        'design_capacity': design_capacity_data,
        'design_capacity_units': design_capacity_units_data
    })
    
    # Filter for the target unit and remove NaN values
    df_filtered = df[
        (df['design_capacity_units'] == target_unit) &
        (df['design_capacity'].notna()) &
        (df['stkhgt'].notna())
    ].copy()
    
    if df_filtered.empty:
        print(f"No data found for unit '{target_unit}'")
        return None
    
    print(f"Found {len(df_filtered)} records with {target_unit} units")
    print(f"Design capacity range: {df_filtered['design_capacity'].min():.2f} - {df_filtered['design_capacity'].max():.2f} {target_unit}")
    
    # Create capacity bins - adjust based on the data range
    capacity_max = df_filtered['design_capacity'].max()
    
    # Create reasonable bins based on the data range
    if capacity_max <= 100:
        bins = [0, 25, 50, 75, 100, float('inf')]
        labels = ['0-25', '25-50', '50-75', '75-100', '>100']
    elif capacity_max <= 500:
        bins = [0, 50, 100, 200, 300, 500, float('inf')]
        labels = ['0-50', '50-100', '100-200', '200-300', '300-500', '>500']
    elif capacity_max <= 1000:
        bins = [0, 100, 200, 400, 600, 800, 1000, float('inf')]
        labels = ['0-100', '100-200', '200-400', '400-600', '600-800', '800-1000', '>1000']
    else:
        bins = [0, 200, 500, 1000, 2000, 5000, float('inf')]
        labels = ['0-200', '200-500', '500-1000', '1000-2000', '2000-5000', '>5000']
    
    # Create capacity categories
    df_filtered['capacity_category'] = pd.cut(df_filtered['design_capacity'], 
                                            bins=bins, 
                                            labels=labels, 
                                            include_lowest=True)
    
    # Remove any categories with no data
    valid_categories = df_filtered['capacity_category'].dropna().unique()
    if len(valid_categories) == 0:
        print("No valid capacity categories found after binning")
        return None
    
    # Create subplots
    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.5])

    # Scatter plot in top row
    ax_scatter = fig.add_subplot(gs[0, :])
    scatter = ax_scatter.scatter(df_filtered['design_capacity'], df_filtered['stkhgt'], 
                               alpha=0.6, s=20)
    ax_scatter.set_xlabel(f'Design Capacity ({target_unit})')
    ax_scatter.set_ylabel('Stack Height (m)')
    ax_scatter.set_title(f'Stack Height vs Design Capacity ({target_unit})')
    ax_scatter.grid(True, alpha=0.3)

    # Box plots in bottom row
    ax_box = fig.add_subplot(gs[1, :])
    
    # Prepare data for box plot
    box_data = []
    box_labels = []
    
    # Sort categories based on the lower bound of each range
    sorted_categories = sorted(valid_categories, key=lambda x: float(x.split('-')[0]))
    
    for category in sorted_categories:
        category_data = df_filtered[df_filtered['capacity_category'] == category]['stkhgt']
        if len(category_data) > 0:
            box_data.append(category_data)
            box_labels.append(f"{category} {target_unit}\n(n={len(category_data)})")
    
    # Create box plot
    bp = ax_box.boxplot(box_data, labels=box_labels)
    ax_box.set_ylabel('Stack Height (m)')
    ax_box.set_title(f'Stack Height Distribution by Design Capacity Bins ({target_unit})')
    ax_box.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.setp(ax_box.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    
    # Create save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Save the plot
    save_path = os.path.join(save_dir, filename)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    # Create statistics DataFrame for CSV export
    stats_data = []
    
    # Add overall statistics
    overall_stats = df_filtered['stkhgt'].describe()
    stats_data.append({
        'category': f'All {target_unit}',
        'count': int(overall_stats['count']),
        'min': overall_stats['min'],
        '25th_percentile': overall_stats['25%'],
        'median': overall_stats['50%'],
        'mean': overall_stats['mean'],
        '75th_percentile': overall_stats['75%'],
        'max': overall_stats['max'],
        'std': overall_stats['std']
    })
    
    # Add statistics for each capacity category
    for category in sorted_categories:
        category_data = df_filtered[df_filtered['capacity_category'] == category]['stkhgt']
        if len(category_data) > 0:
            stats = category_data.describe()
            stats_data.append({
                'category': f'{category} {target_unit}',
                'count': int(stats['count']),
                'min': stats['min'],
                '25th_percentile': stats['25%'],
                'median': stats['50%'],
                'mean': stats['mean'],
                '75th_percentile': stats['75%'],
                'max': stats['max'],
                'std': stats['std']
            })
    
    # Create and save statistics DataFrame
    stats_df = pd.DataFrame(stats_data)
    
    # Generate CSV filename based on the plot filename
    csv_filename = filename.replace('.png', '_stats.csv')
    csv_path = os.path.join(save_dir, csv_filename)
    stats_df.to_csv(csv_path, index=False)
    
    print(f"\nStatistics saved to: {csv_path}")
    print(f"Plot saved to: {save_path}")

    # Print summary statistics for each capacity category
    print(f"\nSummary statistics by design capacity ({target_unit}) category:")
    print("\nAll data:")
    print(df_filtered['stkhgt'].describe())
    
    for category in sorted_categories:
        category_data = df_filtered[df_filtered['capacity_category'] == category]['stkhgt']
        if len(category_data) > 0:
            print(f"\nCategory {category} {target_unit} (n={len(category_data)}):")
            print(category_data.describe())
    
    return df_filtered
