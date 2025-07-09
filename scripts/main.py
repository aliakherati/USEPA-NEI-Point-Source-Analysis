import pandas as pd
import numpy as np
from pathlib import Path
import os
import matplotlib.pyplot as plt
import seaborn as sns
from process import filter_scc_data, filter_poll_data
from read_data import DataReader
from plot import plot_stack_height_analysis

# Define constants
SAVE_DIR = Path("plots")
INPUT_DIR = Path("data/2022hc_cb6_22m/inputs")
SCC_DIR = Path("data")
SCC_FILENAME = "SCCDownload-2025-0708-202427.csv"

# Define analysis categories
ANALYSIS_CATEGORIES = {
    "iron-and-steel": {
        "keywords": ["iron", "steel"],
        "scc_level": 3,
        "pollutant": "PM25-PRI"
    },
    "aluminum": {
        "keywords": ["aluminum"],
        "scc_level": 3,
        "pollutant": "PM25-PRI"
    }
}

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

if __name__ == "__main__":
    # Read data
    data_reader = DataReader(data_dir=INPUT_DIR, scc_dir=SCC_DIR, scc_filename=SCC_FILENAME)
    data_reader.read_and_combine_data()
    data_reader.read_scc_data()

    # Print dataframes
    print(f"\nCombined dataframe shape: {data_reader.combined_df.shape}")
    print(f"\nCombined dataframe head: {data_reader.combined_df.head()}")
    print(f"\nSCC dataframe shape: {data_reader.df_scc.shape}")
    print(f"\nSCC dataframe head: {data_reader.df_scc.head()}\n")

    # Analyze stack heights for each category
    for category, params in ANALYSIS_CATEGORIES.items():
        analyze_stack_heights(
            data_reader,
            keywords=params["keywords"],
            scc_level=params["scc_level"],
            pollutant=params["pollutant"],
            save_dir=SAVE_DIR,
            filename=f"stack_height_analysis_{category}.png"
        )
