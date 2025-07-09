# Analyzing Point Sources from USEPA NEI
The goal of this repo is using any version of National Emission Inventory (NEI) to analyze on the stack height for each industry. The way it works is that:
1. Specify which industry you would like to explore (e.g. iron-and-steel)
2. Choose key words for the desired industry (e.g. `iron` and `steel`)
3. Specify SCC levels where you want the keyword search happens
4. Specify the desired pollutant (e.g. `PM25_PRI`, `PM25_FIL`, `NOx`, `SO2`)
The code will look for active sources in SCC list and search within specified SCC levels based on the keyword. The 

### Setup Virtual Environment
`Python 3.10.14` is used for this repo. To setup the virtual environment please follow these steps:
1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install --upgrade pip`
4. `pip install -r requirements.txt`

### Repository Structure

The repository is organized as follows:

- `data/`: Directory containing input data files
  - `2022hc_cb6_22m/inputs/`: Contains CSV files with point source data
  - `SCCDownload-2025-0708-202427.csv`: Source Classification Code (SCC) reference data

- `scripts/`: Python scripts for data processing and analysis
  - `main.py`: Main script that orchestrates the data processing workflow
  - `read_data.py`: Contains `DataReader` class for reading and combining CSV files
  - `process.py`: Functions for filtering SCC and pollutant data

- `requirements.txt`: Lists all Python package dependencies
- `.venv/`: Python virtual environment directory (created during setup)

The code reads point source emissions data from CSV files, combines them, and provides filtering capabilities based on Source Classification Codes (SCC) and pollutant types. The `DataReader` class handles file reading and data combination, while separate processing functions in `process.py` handle data filtering and analysis.
