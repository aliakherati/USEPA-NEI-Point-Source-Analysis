import pandas as pd
import numpy as np
from pathlib import Path
import os
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import yaml
from process import filter_scc_data, filter_poll_data, filter_poll_data_with_capacity
from read_data import DataReader
from plot import plot_stack_height_analysis, plot_stack_height_by_capacity

def load_config(config_path: str) -> dict:
    """
    Load configuration from YAML file.
    
    Parameters
    ----------
    config_path : str
        Path to the YAML configuration file
        
    Returns
    -------
    dict
        Configuration dictionary
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def analyze_stack_heights(
    data_reader: DataReader,
    keywords: list[str],
    scc_level: int,
    pollutant: str,
    save_dir: Path,
    filename: str,
):
    """
    Analyze stack heights by filtering SCC data and creating visualizations.
    
    Parameters
    ----------
    data_reader : DataReader
        DataReader instance containing the combined and SCC dataframes
    keywords : list of str
        Keywords to filter SCC data
    scc_level : int
        SCC level to filter on
    pollutant : str
        Pollutant to analyze
    save_dir : Path
        Directory to save plots
    filename : str
        Name of output plot file
    """
    # Filter SCC data
    filtered_df = filter_scc_data(data_reader.df_scc, keywords=keywords, scc_level=scc_level)
    print(f"\nFiltered SCC dataframe shape: {filtered_df.shape}")
    print(f"\nFiltered SCC dataframe head: {filtered_df.head()}\n")

    scc_set = set(filtered_df['SCC'].astype(int))

    # Filter for pollutant and scc numbers from filtered scc dataframe and get rid of nan values for stack height
    stkhgt_data = filter_poll_data(data_reader.combined_df, pollutant, scc_set)['stkhgt']

    # Plot stack height analysis
    plot_stack_height_analysis(stkhgt_data, save_dir=save_dir, filename=filename)

    # Create bins for stack height categories
    categories = pd.cut(stkhgt_data,
                       bins=[0, 10, 100, float('inf')],
                       labels=['0-10', '10-100', '>100'])
    
    # Define category mappings
    category_data = [
        (stkhgt_data, 'All'),
        (stkhgt_data[categories == '0-10'], '0-10m'),
        (stkhgt_data[categories == '10-100'], '10-100m'), 
        (stkhgt_data[categories == '>100'], '>100m')
    ]

    # Get stats for all data and each category
    stats_text = []
    for data, label in category_data:
        stats = data.describe()
        stats_text.append([
            stats['max'],
            stats['min'], 
            stats['mean'],
            stats['50%'],
            stats['25%'],
            stats['75%'],
            stats['std'],
            label
        ])
    return [stats_text]

def analyze_stack_heights_by_capacity(
    data_reader: DataReader,
    keywords: list[str],
    scc_level: int,
    pollutant: str,
    target_unit: str = "MW",
    save_dir: Path = Path("plots"),
    filename: str = "stack_height_by_capacity.png"
):
    """
    Analyze stack heights by design capacity for a specific industry category.
    
    Parameters
    ----------
    data_reader : DataReader
        DataReader instance containing the combined and SCC dataframes
    keywords : list of str
        Keywords to filter SCC data
    scc_level : int
        SCC level to filter on
    pollutant : str
        Pollutant to analyze
    target_unit : str
        Design capacity unit to filter for (e.g., "MW")
    save_dir : Path
        Directory to save plots
    filename : str
        Name of output plot file
    """
    # Filter SCC data
    filtered_df = filter_scc_data(data_reader.df_scc, keywords=keywords, scc_level=scc_level)
    print(f"\nFiltered SCC dataframe shape: {filtered_df.shape}")
    
    if filtered_df.empty:
        print("No SCC data found for the given keywords and level")
        return None

    scc_set = set(filtered_df['SCC'].astype(int))

    # Filter for pollutant, scc numbers, and get design capacity data
    try:
        capacity_data = filter_poll_data_with_capacity(data_reader.combined_df, pollutant, scc_set)
        print(f"\nFiltered capacity data shape: {capacity_data.shape}")
        
        if capacity_data.empty:
            print("No data found for the given pollutant and SCC codes")
            return None
            
    except ValueError as e:
        print(f"Error filtering data: {e}")
        return None

    # Plot stack height analysis by capacity
    result_df = plot_stack_height_by_capacity(
        stkhgt_data=capacity_data['stkhgt'],
        design_capacity_data=capacity_data['design_capacity'],
        design_capacity_units_data=capacity_data['design_capacity_units'],
        target_unit=target_unit,
        save_dir=save_dir,
        filename=filename
    )
    
    return result_df

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Analyze stack heights for different industrial categories')
    parser.add_argument('--config', type=str, required=True, 
                       help='Path to the YAML configuration file')
    parser.add_argument('--capacity-analysis', action='store_true',
                       help='Run capacity analysis in addition to standard analysis')
    parser.add_argument('--target-unit', type=str, default='MW',
                       help='Target unit for capacity analysis (default: MW)')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Extract configuration values
    data_config = config['data']
    analysis_categories = config['analysis_categories']
    
    # Define paths from config
    save_dir = Path(data_config['save_dir'])
    input_dir = Path(data_config['input_dir'])
    scc_dir = Path(data_config['scc_dir'])
    scc_filename = data_config['scc_filename']
    
    # Create save directory if it doesn't exist
    save_dir.mkdir(exist_ok=True)
    
    # Read data
    data_reader = DataReader(data_dir=input_dir, scc_dir=scc_dir, scc_filename=scc_filename)
    data_reader.read_and_combine_data()
    data_reader.read_scc_data()

    # Print dataframes
    print(f"\nCombined dataframe shape: {data_reader.combined_df.shape}")
    print(f"\nCombined dataframe head: {data_reader.combined_df.head()}")
    print(f"\nSCC dataframe shape: {data_reader.df_scc.shape}")
    print(f"\nSCC dataframe head: {data_reader.df_scc.head()}\n")

    # Analyze stack heights for each category
    stats_text = []
    for category, params in analysis_categories.items():
        stats = analyze_stack_heights(
            data_reader,
            keywords=params["keywords"],
            scc_level=params["scc_level"],
            pollutant=params["pollutant"],
            save_dir=save_dir,
            filename=f"stack_height_analysis_{category}.png"
        )[0]  # Extract inner list
        for stat in stats:
            stat.append(category)  # Add category to each stat row
        stats_text.extend(stats)

    pd.DataFrame(stats_text, columns=["Max", "Min", "Mean", "Median", "25%", "75%", "Std", "height bin", "category"]).to_csv(save_dir / "stack_height_stats.csv")

    # Run capacity analysis if requested
    if args.capacity_analysis:
        print("\n" + "="*60)
        print("RUNNING CAPACITY ANALYSIS")
        print("="*60)
        
        for category, params in analysis_categories.items():
            print(f"\nAnalyzing {category} category by capacity...")
            result_df = analyze_stack_heights_by_capacity(
                data_reader=data_reader,
                keywords=params["keywords"],
                scc_level=params["scc_level"],
                pollutant=params["pollutant"],
                target_unit=args.target_unit,
                save_dir=save_dir,
                filename=f"stack_height_by_capacity_{category}.png"
            )
            
            if result_df is not None:
                print(f"Capacity analysis complete for {category}!")
                print(f"Total records analyzed: {len(result_df)}")
                print(f"CSV statistics file: stack_height_by_capacity_{category}_stats.csv")
            else:
                print(f"Capacity analysis failed for {category} category")
        
        print(f"\nCapacity analysis complete! Check the '{save_dir}' directory for:")
        print("- PNG plot files: stack_height_by_capacity_[category].png")
        print("- CSV statistics files: stack_height_by_capacity_[category]_stats.csv")

if __name__ == "__main__":
    main()
