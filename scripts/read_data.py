import pandas as pd
import numpy as np
from pathlib import Path
import os

class DataReader:
    def __init__(self, data_dir: Path, scc_dir: Path, scc_filename: str):
        self.scc_dir = scc_dir
        self.data_dir = data_dir
        self.scc_filename = scc_filename
        self.csv_files = self._get_csv_files(self.data_dir)
        self.combined_df = None
        self.df_scc = None

    def _get_csv_files(self, directory):
        """Recursively get all CSV files in directory and subdirectories"""
        csv_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))
        return csv_files

    def _read_csv_with_comments(self, filepath):
        """Read CSV file, handling comment lines at the start"""
        # Count comment lines to skip
        with open(filepath, 'r') as f:
            skip_lines = 0
            for line in f:
                if line.startswith('#'):
                    skip_lines += 1
                else:
                    break
                    
        # Read CSV skipping comment lines
        return pd.read_csv(filepath, skiprows=skip_lines)

    def print_directory_structure(self):
        """Print directory tree structure"""
        print("Data directory structure:")
        for root, dirs, files in os.walk(self.data_dir):
            level = root.replace(str(self.data_dir), '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = '  ' * (level + 1)
            for f in files:
                if f.endswith('.csv'):
                    print(f"{subindent}{f}")

    def read_and_combine_data(self):
        """Read and concatenate all CSV files"""
        dataframes = []
        for i, csv_file in enumerate(self.csv_files):
            try:
                print(f"{i}/{len(self.csv_files)}: Reading {csv_file}")
                df = self._read_csv_with_comments(csv_file)
                dataframes.append(df)
                print(f"Successfully read: {csv_file}")
            except Exception as e:
                print(f"Error reading {csv_file}: {str(e)}")

        if dataframes:
            self.combined_df = pd.concat(dataframes, ignore_index=True)
            # Remove rows that are all NaN
            self.combined_df = self.combined_df.dropna(how='all')
            # Convert scc to integer and stkhgt to float
            self.combined_df['scc'] = self.combined_df['scc'].astype('Int64')  # Int64 allows for NaN values
            self.combined_df['stkhgt'] = self.combined_df['stkhgt'].astype('float64')
            print(f"\nCombined {len(dataframes)} CSV files into dataframe with shape: {self.combined_df.shape}")
        else:
            print("\nNo CSV files were successfully read")

    def read_scc_data(self):
        """Read SCC data file"""
        filepath = self.scc_dir / self.scc_filename
        self.df_scc = pd.read_csv(filepath)