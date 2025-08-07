#!/usr/bin/env python3
"""
Test script for the new capacity analysis functionality.

This script creates sample data and tests the plot_stack_height_by_capacity function.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add the scripts directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from plot import plot_stack_height_by_capacity


def create_sample_data():
    """Create sample data for testing the capacity analysis function."""
    np.random.seed(42)  # For reproducible results
    
    # Create sample data with different capacity ranges
    n_samples = 1000
    
    # Generate design capacity values (MW)
    capacity_values = np.concatenate([
        np.random.uniform(0, 50, 300),      # Small units
        np.random.uniform(50, 200, 400),    # Medium units  
        np.random.uniform(200, 500, 200),   # Large units
        np.random.uniform(500, 1000, 100)   # Very large units
    ])
    
    # Generate corresponding stack heights (correlated with capacity)
    stack_heights = 20 + 0.1 * capacity_values + np.random.normal(0, 10, n_samples)
    stack_heights = np.maximum(stack_heights, 5)  # Minimum stack height of 5m
    
    # Create units (mostly MW, some other units)
    units = np.random.choice(['MW', 'KW', 'HP'], size=n_samples, p=[0.8, 0.15, 0.05])
    
    # Create the sample dataframe
    sample_data = pd.DataFrame({
        'stkhgt': stack_heights,
        'design_capacity': capacity_values,
        'design_capacity_units': units
    })
    
    return sample_data


def test_capacity_analysis():
    """Test the capacity analysis function with sample data."""
    print("Creating sample data...")
    sample_data = create_sample_data()
    
    print(f"Sample data shape: {sample_data.shape}")
    print(f"Capacity range: {sample_data['design_capacity'].min():.2f} - {sample_data['design_capacity'].max():.2f}")
    print(f"Stack height range: {sample_data['stkhgt'].min():.2f} - {sample_data['stkhgt'].max():.2f}")
    print(f"Available units: {sample_data['design_capacity_units'].unique()}")
    
    # Test with MW units
    print("\n" + "="*50)
    print("TESTING MW CAPACITY ANALYSIS")
    print("="*50)
    
    result_df = plot_stack_height_by_capacity(
        stkhgt_data=sample_data['stkhgt'],
        design_capacity_data=sample_data['design_capacity'],
        design_capacity_units_data=sample_data['design_capacity_units'],
        target_unit="MW",
        save_dir="test_plots",
        filename="test_stack_height_by_capacity_MW.png"
    )
    
    if result_df is not None:
        print(f"\nMW analysis successful!")
        print(f"Records analyzed: {len(result_df)}")
        print(f"Capacity categories found: {result_df['capacity_category'].unique()}")
    else:
        print("\nMW analysis failed!")
    
    # Test with KW units
    print("\n" + "="*50)
    print("TESTING KW CAPACITY ANALYSIS")
    print("="*50)
    
    result_df = plot_stack_height_by_capacity(
        stkhgt_data=sample_data['stkhgt'],
        design_capacity_data=sample_data['design_capacity'],
        design_capacity_units_data=sample_data['design_capacity_units'],
        target_unit="KW",
        save_dir="test_plots",
        filename="test_stack_height_by_capacity_KW.png"
    )
    
    if result_df is not None:
        print(f"\nKW analysis successful!")
        print(f"Records analyzed: {len(result_df)}")
        print(f"Capacity categories found: {result_df['capacity_category'].unique()}")
    else:
        print("\nKW analysis failed!")
    
    # Test with non-existent unit
    print("\n" + "="*50)
    print("TESTING NON-EXISTENT UNIT")
    print("="*50)
    
    result_df = plot_stack_height_by_capacity(
        stkhgt_data=sample_data['stkhgt'],
        design_capacity_data=sample_data['design_capacity'],
        design_capacity_units_data=sample_data['design_capacity_units'],
        target_unit="NONEXISTENT",
        save_dir="test_plots",
        filename="test_stack_height_by_capacity_nonexistent.png"
    )
    
    if result_df is not None:
        print(f"\nNon-existent unit analysis should have failed but didn't!")
    else:
        print("\nNon-existent unit analysis correctly failed!")


if __name__ == "__main__":
    test_capacity_analysis() 