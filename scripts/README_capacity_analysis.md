# Stack Height Analysis by Design Capacity

This document explains how to use the new capacity analysis functionality that allows you to analyze stack heights binned by design capacity for different units (e.g., MW, KW, HP).

## Overview

The new functionality extends the existing stack height analysis by adding the ability to:
1. Filter data by design capacity units (e.g., "MW" for megawatts)
2. Bin the data by design capacity ranges
3. Create box plots showing stack height distributions for each capacity bin
4. Generate scatter plots showing the relationship between design capacity and stack height
5. Provide detailed statistics for each capacity bin
6. **Export statistics to CSV files for further analysis**

## New Functions

### `plot_stack_height_by_capacity()`

**Location**: `scripts/plot.py`

**Parameters**:
- `stkhgt_data`: pandas.Series containing stack height measurements in meters
- `design_capacity_data`: pandas.Series containing design capacity values
- `design_capacity_units_data`: pandas.Series containing design capacity units
- `target_unit`: str, unit to filter for (default: "MW")
- `save_dir`: str, directory to save plots (default: "../plots")
- `filename`: str, name of output plot file (default: "stack_height_by_capacity.png")

**Returns**: pandas.DataFrame with filtered data and capacity categories

**Outputs**:
- PNG plot file with scatter plot and box plots
- CSV file with detailed statistics for each capacity category

### `filter_poll_data_with_capacity()`

**Location**: `scripts/process.py`

**Parameters**:
- `df`: pandas.DataFrame, input dataframe to filter
- `poll`: str or list of str, pollutant(s) to filter for
- `scc_set`: set, set of SCC codes to filter for

**Returns**: pandas.DataFrame with stkhgt, design_capacity, and design_capacity_units columns

## Usage Examples

### 1. Using the Main Script with Capacity Analysis

Run the main analysis script with capacity analysis enabled:

```bash
# Run standard analysis plus capacity analysis for MW units
python scripts/main.py --config configs/sources.yaml --capacity-analysis --target-unit MW

# Run with different units
python scripts/main.py --config configs/sources.yaml --capacity-analysis --target-unit KW
```

### 2. Using the Example Script

Run the dedicated example script:

```bash
python scripts/example_capacity_analysis.py
```

### 3. Using the Functions Directly

```python
from scripts.plot import plot_stack_height_by_capacity
from scripts.process import filter_poll_data_with_capacity

# Filter data to get capacity information
capacity_data = filter_poll_data_with_capacity(df, pollutant, scc_set)

# Create capacity analysis plots
result_df = plot_stack_height_by_capacity(
    stkhgt_data=capacity_data['stkhgt'],
    design_capacity_data=capacity_data['design_capacity'],
    design_capacity_units_data=capacity_data['design_capacity_units'],
    target_unit="MW",
    save_dir="plots",
    filename="my_capacity_analysis.png"
)
```

## Output

The function generates:

1. **Scatter Plot**: Shows the relationship between design capacity and stack height
2. **Box Plot**: Shows stack height distributions for each capacity bin
3. **Statistics**: Detailed statistics for each capacity category including:
   - Count of records
   - Mean, median, min, max
   - 25th and 75th percentiles
   - Standard deviation
4. **CSV File**: Exports all statistics to a CSV file for further analysis

### CSV Output Format

The CSV file contains the following columns:
- `category`: Capacity category (e.g., "0-100 MW", "100-200 MW")
- `count`: Number of records in the category
- `min`: Minimum stack height in the category
- `25th_percentile`: 25th percentile of stack heights
- `median`: Median stack height
- `mean`: Average stack height
- `75th_percentile`: 75th percentile of stack heights
- `max`: Maximum stack height in the category
- `std`: Standard deviation of stack heights

**Example CSV output**:
```csv
category,count,min,25th_percentile,median,mean,75th_percentile,max,std
All MW,811,5.0,24.63,34.90,41.05,49.95,126.13,24.14
0-100 MW,346,5.0,18.46,25.49,25.31,31.48,48.36,9.16
100-200 MW,215,5.34,27.33,35.34,35.05,42.26,64.39,10.71
...
```

## Capacity Binning

The function automatically creates appropriate bins based on the data range:

- **Small range (≤100)**: 0-25, 25-50, 50-75, 75-100, >100
- **Medium range (≤500)**: 0-50, 50-100, 100-200, 200-300, 300-500, >500
- **Large range (≤1000)**: 0-100, 100-200, 200-400, 400-600, 600-800, 800-1000, >1000
- **Very large range (>1000)**: 0-200, 200-500, 500-1000, 1000-2000, 2000-5000, >5000

## Available Units

Common design capacity units in the data include:
- **MW**: Megawatts (most common for power plants)
- **KW**: Kilowatts
- **HP**: Horsepower
- **E6BTU/HR**: Million BTU per hour
- **E3LB/HR**: Thousand pounds per hour
- **FT3/DAY**: Cubic feet per day
- **BLRHP**: Boiler horsepower
- **GAL**: Gallons

## Testing

Run the test script to verify functionality:

```bash
python scripts/test_capacity_function.py
```

This will create sample data and test the function with different units, generating test plots in the `test_plots/` directory and CSV statistics files.

## Integration with Existing Workflow

The capacity analysis integrates seamlessly with the existing workflow:

1. **SCC Filtering**: Uses the same SCC filtering logic as the standard analysis
2. **Pollutant Filtering**: Filters by the same pollutants
3. **Data Processing**: Uses the same data reader and processing pipeline
4. **Configuration**: Uses the same YAML configuration files

The only difference is that it also extracts and analyzes design capacity information.

## File Naming Convention

When you run the capacity analysis, the following files are generated:

- **Plot files**: `stack_height_by_capacity_[category].png`
- **Statistics files**: `stack_height_by_capacity_[category]_stats.csv`

For example, if you analyze the "electricity" category with MW units:
- `stack_height_by_capacity_electricity.png`
- `stack_height_by_capacity_electricity_stats.csv` 