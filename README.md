# Analyzing Point Sources in the US EPA National Emissions Inventory (NEI)

> **Goal:** Quickly extract, filter, and analyze point-source emissions (e.g., stack heights) for any industry and pollutant in any NEI release.

---

## ✨ Key Features

| Feature                       | What it does                                                                                                                            |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Flexible keyword search**   | Identify relevant Source Classification Codes (SCCs) with user-supplied keywords at any SCC level.                                      |
| **Industry-specific queries** | Target a single industry (e.g., _Iron & Steel_) or compare several side-by-side.                                                        |
| **Pollutant filtering**       | Focus on one or many pollutants (`PM25_PRI`, `PM25_FIL`, `NOx`, `SO₂`, …).                                                              |
| **End-to-end workflow**       | One command ingests raw NEI CSVs, filters SCCs, joins them to emissions data, and exports a tidy dataframe or visualization-ready file. |
| **Pythonic & reproducible**   | Pure-Python project (3.10+) with `pandas` and `polars` back-ends, managed in a virtual environment.                                     |

---

## 🗺️ How It Works

1. **Select an industry**  
   Define a human-readable name, e.g. `"iron-and-steel"`.
2. **Provide search keywords**  
   Any number of terms (`["iron", "steel"]`) matched **case-insensitively** inside SCC descriptions.
3. **Choose SCC levels**  
   Tell the script which parts of the hierarchical SCC to search (`LEVEL_TWO`, `LEVEL_THREE`, …).
4. **Pick pollutants**  
   List one or more pollutant codes (`["PM25_PRI"]`).
5. **Run `scripts/main.py`**  
   The workflow:
   ```text
   ┌─► Download / read SCC list (CSV)
   ├─► Filter SCCs by keyword + “Active” status + “Point” sources
   ├─► Read NEI point-source CSVs
   ├─► Sub-select chosen pollutants
   └─► Plot results
   ```

## ⚡ Quick-Start

### 1. Clone the repo

```bash
git clone https://github.com/aliakherati/USEPA-NEI-Point-Source-Analysis.git
cd USEPA-NEI-Point-Source-Analysis
```

### 2. Create & activate a virtual environment (Python 3.10+)

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the example workflow

```bash
python scripts/main.py --config configs/sources.yaml
```

## 🏗️ Repository Layout

```bash
.
├── data/                       # <- Raw & processed data (git-ignored by default)
│   └── 2022hc_cb6_22m/inputs/  #    NEI 2022 point-source CSVs
├── scripts/
│   ├── main.py                 # Workflow orchestrator (entry point)
│   ├── read_data.py            # DataReader class (lazy CSV reader / concatenator)
│   ├── plot.py                 # Stack height visualization utilities
│   └── process.py              # SCC & pollutant filtering utilities
├── configs/                    # YAML example for repeatable analyses
├── requirements.txt
└── README.md
```

## 🔧 Configuration

Instead of editing code, place run-time options in a simple YAML file:

```yaml
# Data paths
data:
  save_dir: "plots"
  input_dir: "data/2022hc_cb6_22m/inputs"
  scc_dir: "data"
  scc_filename: "SCCDownload-2025-0708-202427.csv"

# Analysis categories
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

Invoke with:

```bash
python scripts/main.py --config configs/sources.yml
```

📊 Data Sources
| Dataset | URL |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **NEI point-source emissions (2022, v1)** | [https://gaftp.epa.gov/Air/emismod/2022/v1/2022emissions/](https://gaftp.epa.gov/Air/emismod/2022/v1/2022emissions/) |
| **Source Classification Codes (SCC)** | [https://sor-scc-api.epa.gov/sccwebservices/sccsearch/](https://sor-scc-api.epa.gov/sccwebservices/sccsearch/) |

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

## 🗨️ Contact

Maintainer • Ali Akherati • aliakherati@outlook.com
Feel free to reach out with questions, bug reports, or suggestions.
