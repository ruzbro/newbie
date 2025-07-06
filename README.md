# Greenhouse Performance Analysis

This project analyzes greenhouse performance based on harvest, revenue, and environmental data. It includes Python scripts to process the data, generate analytical summaries, and create visualizations.

## Analysis Summary

This project introduces two Python scripts for analyzing and visualizing greenhouse performance:

- **`analyze_greenhouse.py`**:
  - Loads data from `data/Revenue by Greenhouse by Crop.csv`.
  - Calculates and plots the total kilograms harvested per week for each greenhouse using Matplotlib.
  - Filters out data from future harvest dates to provide an accurate historical analysis.
  - Outputs a summary of the best-performing greenhouse to the console.

- **`create_plotly_chart.py`**:
  - Generates an interactive, stacked area chart using Plotly.
  - The chart stacks greenhouses based on total harvest volume (highest at the bottom).
  - Features a pastel color scheme and a customized legend.
  - Saves the resulting visualization as an HTML file (`greenhouse_harvest_stacked_area.html`).

## Data Files

The analysis is based on the following three datasets:

### 1. `Revenue by Greenhouse by Crop.csv`
This file contains financial and yield data, comparing actuals against targets for various crops in different greenhouses.

| Column | Description |
| :--- | :--- |
| `resource_tag` | Identifier for the greenhouse (e.g., GH1, GH2). |
| `crop_name` | The name of the crop. |
| `harvest_week_num` | The week of harvest in YYYY-WW format. |
| `week_label` | A human-readable label for the harvest week (e.g., Mar-03 w10). |
| `b2b_b_target_revenue`| The target revenue from B2B business channels. |
| `hotel_b_target_revenue`| The target revenue from hotel business channels. |
| `b2b_b_harvest_revenue`| The actual revenue from B2B business channels. |
| `hotel_b_harvest_revenue`| The actual revenue from hotel business channels. |
| `target_kg` | The target harvest weight in kilograms. |
| `kg_harvested` | The actual harvested weight in kilograms. |
| `pct_of_target_kg` | The percentage of the target weight achieved. |
| `target_unit_g` | The target weight per unit in grams. |
| `harvest_unit_g` | The actual weight per unit in grams. |
| `pct_of_target_unit_g`| The percentage of the target unit weight achieved. |
| `current_week` | The reference week for which the data was generated. |

### 2. `crop calendar week 10-22.csv`
This file provides a detailed schedule and log of agricultural activities, from seeding to harvesting, for each crop.

| Column | Description |
| :--- | :--- |
| `id` | A unique identifier for the calendar entry. |
| `resource_tag` | Identifier for the greenhouse (e.g., PNQ-GH1). |
| `program_id` | An identifier for the specific growing program. |
| `crop_id` | A numeric identifier for the crop. |
| `group_tag` | A tag grouping related activities, often by year and week. |
| `weekly_harvest_channels`| An identifier for the harvest channels. |
| `alloc_date` | The date the activity was allocated. |
| `seeding_date` | The date the seeds were planted. |
| `target_seedlings` | The target number of seedlings for the batch. |
| `transplant_date` | The date the seedlings were transplanted. |
| `harvest_date` | The scheduled or actual date of harvest. |
| `activity_status` | The current status of the activity (e.g., PGM_SIMULATION, ALLOCATED). |
| `seeding_rows` | The number of rows seeded. |
| `harvest_units` | The number of units expected or harvested. |
| `harvest_week_num` | The week of harvest in YYYY-WW format. |
| `kg_harvested` | The actual weight harvested in kilograms. |
| `units_harvested` | The actual number of units harvested. |

### 3. `Hydronomics Data - GH1.csv`
This file contains time-series data of environmental metrics recorded in Greenhouse 1 (GH1), such as pH and electrical conductivity (EC).

| Column | Description |
| :--- | :--- |
| `metric_code` | The code for the environmental metric being measured (e.g., `sys_ec`, `sys_ph`). |
| `date_time` | The specific date and time the measurement was recorded. |
| `week_num` | The week number in YYYY-WW format. |
| `value` | The recorded value of the metric. |
| `location_code` | The location where the measurement was taken (in this file, GH1). |


## How to Run the Analysis

To run the analysis scripts, you first need to install the required Python packages.

**1. Install Dependencies:**
```bash
# For the Matplotlib-based analysis
pip install pandas matplotlib

# For the Plotly-based analysis
pip install pandas plotly
```

**2. Run the Scripts:**
```bash
# To generate the static line chart
python3 analyze_greenhouse.py

# To generate the interactive HTML chart
python3 create_plotly_chart.py
```

## Outputs

- **`greenhouse_weekly_harvest_past_only.png`**: A static PNG image of the weekly harvest performance.
- **`greenhouse_harvest_stacked_area.html`**: An interactive HTML file containing the stacked area chart of weekly harvests. 