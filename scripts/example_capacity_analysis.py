#!/usr/bin/env python3
"""
Example script demonstrating stack height analysis by design capacity.

This script shows how to use the new plot_stack_height_by_capacity function
to analyze stack heights binned by design capacity for different units (e.g., MW).
"""

import pandas as pd
import yaml
from pathlib import Path
import sys
import os

# Add the scripts directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from read_data import DataReader
from process import filter_scc_data, filter_poll_data_with_capacity
from plot import plot_stack_height_by_capacity


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def analyze_stack_heights_by_capacity(
    data_reader: DataReader,
    keywords: list[str],
    scc_level: int,
    pollutant: str,
    target_unit: str = "MW",
    save_dir: Path = Path("../plots"),
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
    """Main function to run the capacity analysis example."""
    # Load configuration
    config_path = "../configs/sources.yaml"
    config = load_config(config_path)
    
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
    print("Reading data...")
    data_reader = DataReader(data_dir=input_dir, scc_dir=scc_dir, scc_filename=scc_filename)
    data_reader.read_and_combine_data()
    data_reader.read_scc_data()
    
    print(f"Combined dataframe shape: {data_reader.combined_df.shape}")
    print(f"SCC dataframe shape: {data_reader.df_scc.shape}")

    # Analyze stack heights by capacity for electricity category (which likely has MW units)
    print("\n" + "="*60)
    print("ANALYZING STACK HEIGHTS BY DESIGN CAPACITY")
    print("="*60)
    
    # Example: Analyze electricity category with MW units
    if 'electricity' in analysis_categories:
        category = 'electricity'
        params = analysis_categories[category]
        
        print(f"\nAnalyzing {category} category...")
        result_df = analyze_stack_heights_by_capacity(
            data_reader=data_reader,
            keywords=params["keywords"],
            scc_level=params["scc_level"],
            pollutant=params["pollutant"],
            target_unit="MW",
            save_dir=save_dir,
            filename=f"stack_height_by_capacity_{category}.png"
        )
        
        if result_df is not None:
            print(f"\nAnalysis complete! Plot saved as: stack_height_by_capacity_{category}.png")
            print(f"Total records analyzed: {len(result_df)}")
        else:
            print(f"Analysis failed for {category} category")
    
    # You can also try other units if available
    print("\n" + "="*60)
    print("AVAILABLE DESIGN CAPACITY UNITS")
    print("="*60)
    
    # Check what units are available in the data
    if hasattr(data_reader, 'combined_df') and data_reader.combined_df is not None:
        if 'design_capacity_units' in data_reader.combined_df.columns:
            units = data_reader.combined_df['design_capacity_units'].dropna().unique()
            print("Available design capacity units:")
            for unit in sorted(units):
                count = len(data_reader.combined_df[data_reader.combined_df['design_capacity_units'] == unit])
                print(f"  {unit}: {count} records")
        else:
            print("No 'design_capacity_units' column found in the data")


if __name__ == "__main__":
    main() 