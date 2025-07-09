# Configuration Files

This directory contains YAML configuration files for the CMU Lab analysis scripts.

## Usage

Run the main analysis script with a configuration file:

```bash
python scripts/main.py --config configs/sources.yaml
```

## Configuration File Structure

The configuration file (`sources.yaml`) contains:

### Data Paths
- `save_dir`: Directory where plots will be saved
- `input_dir`: Directory containing input data files
- `scc_dir`: Directory containing SCC data
- `scc_filename`: Name of the SCC CSV file

### Analysis Categories
Each category defines:
- `keywords`: List of keywords to filter SCC data
- `scc_level`: SCC level to filter on (typically 3)
- `pollutant`: Pollutant to analyze (e.g., "PM25-PRI")

## Example Configuration

```yaml
data:
  save_dir: "plots"
  input_dir: "data/2022hc_cb6_22m/inputs"
  scc_dir: "data"
  scc_filename: "SCCDownload-2025-0708-202427.csv"

analysis_categories:
  iron-and-steel:
    keywords: ["iron", "steel"]
    scc_level: 3
    pollutant: "PM25-PRI"
  
  aluminum:
    keywords: ["aluminum"]
    scc_level: 3
    pollutant: "PM25-PRI"
```

## Adding New Categories

To add a new analysis category:

1. Edit the YAML configuration file
2. Add a new category under `analysis_categories`
3. Define the keywords, SCC level, and pollutant
4. Run the script with the updated configuration

Example:
```yaml
cement:
  keywords: ["cement", "concrete"]
  scc_level: 3
  pollutant: "PM25-PRI"
``` 