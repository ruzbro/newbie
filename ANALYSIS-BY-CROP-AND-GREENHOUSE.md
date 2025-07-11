# Analysis by Crop and Greenhouse

## Crop: Arugula, Greenhouse: GH1

### Performance Summary

Arugula production in Greenhouse 1 during the first half of 2025 was significantly below expectations, achieving only **13%** of its targeted harvest weight and revenue. This indicates a severe and persistent issue affecting the crop's growth and yield.

- **Total Target Harvest:** 1664 kg
- **Total Actual Harvest:** 217.2 kg
- **Total Target Revenue:** $1,830,400
- **Total Actual Revenue:** $238,820

The harvest yields were consistently low, with even the best-performing weeks (2025-13 and 2025-14) falling more than 50% short of their targets.

### Root Cause Analysis

The primary cause for this underperformance appears to be a critical systems failure, supported by the following observations from the hydronomics data:

1.  **Critical Electrical Conductivity (EC) Drop:** The most significant anomaly was a drastic drop in the system's Electrical Conductivity (`sys_ec`) to **134** on **February 16th, 2025**. This is a severe deviation from the typical operating range of 800-1300. This event directly preceded the growing cycle for one of the lowest-yielding harvests and would have caused a significant shock to the plants, stunting their growth.

2.  **Inconsistent pH Levels:** The system's pH levels (`sys_ph`) also showed instability, fluctuating between 6.18 and 6.78 during the period of lowest yield. Inconsistent pH can inhibit nutrient absorption and contribute to poor plant health.

3.  **Data Quality Concerns:** The analysis also highlighted several data quality issues, including missing data points and anomalous values for water temperature and greenhouse humidity. These inconsistencies can impede accurate performance monitoring and diagnostics.

## Data Quality and Completeness

During the analysis of the combined Hydronomics data, a dedicated data verification process was implemented to assess the quality and completeness of the sensor readings. A `status` column was added to the `Hydronomics Data Merged.csv` file to flag unusual data points, enabling proactive data integrity management.

### Status Codes for Data Anomalies

The `status` column categorizes data points as follows:

*   **`NULL` (Normal)**: The data point's value falls within the predefined expected range for its metric. This is the expected status for the vast majority of data.
*   **`out-of-range`**: The data point's value is physically impossible or highly improbable for its metric (e.g., pH < 0 or > 14, Relative Humidity > 100%). These are strong indicators of errors.
*   **`low-ec-to-verify`**: Specific to Electrical Conductivity (EC) metrics (`sys_ec` and `fwater_ec`), this status flags values less than 1000. While potentially valid for freshwater or dilute solutions, it warrants verification as typical nutrient solutions often have EC values above 1000.
*   **`non-numeric`**: The recorded value was not a valid number and was coerced to `NaN` during processing, indicating a data entry or encoding issue.

### Key Findings on Data Quality

**Total Anomalies Identified:**
*   `non-numeric`: 1863 occurrences
*   `low-ec-to-verify`: 1048 occurrences
*   `out-of-range`: 41 occurrences

**Metrics with the Most Anomalies:**
*   **`out-of-range`**: `fwater_ph` (Freshwater PH) with 17 occurrences.
*   **`low-ec-to-verify`**: `fwater_ec` (Freshwater EC) with 843 occurrences.
*   **`non-numeric`**: `fwater_temp` (Freshwater Temp) with 291 occurrences.

**Greenhouses with the Most Anomalies:**
*   **`out-of-range`**: `Nursery` with 25 occurrences.
*   **`low-ec-to-verify`**: `Nursery` with 274 occurrences.
*   **`non-numeric`**: `Nursery` with 596 occurrences.

The `Nursery` greenhouse consistently shows the highest number of anomalies across all categories, suggesting potential issues with data collection or sensor calibration in that specific location.

### Data Completeness Analysis (Missing Values)

*   **Greenhouse with the least missing values (most complete):** `GH2` with 284 missing values.
*   **Metric with the most missing values:** `fwater_temp` (Freshwater Temp) with 291 missing values.
*   **Day of the week with the most missing values:** `Monday` with 351 missing values.
*   **Combined (Metric, Greenhouse, Day) with the most missing values:** `('fwater_ec', 'Nursery', 'Monday')` with 31 missing values.

### Ranking of Metrics by Percentage of Normal Readings

The following table ranks metrics by the percentage of readings that fall within their normal, expected ranges (i.e., `NULL` status), from highest to lowest:

| metric_code | total_readings | normal_readings | percentage_normal |
| :---------- | :------------- | :-------------- | :---------------- |
| `sys_gh_temp` | 1085 | 864 | 79.63 |
| `sys_h20_temp` | 1085 | 864 | 79.63 |
| `sys_gh_rh` | 1085 | 863 | 79.54 |
| `sys_ph` | 1085 | 848 | 78.16 |
| `fwater_ph` | 1085 | 841 | 77.51 |
| `fwater_temp` | 1085 | 791 | 72.90 |
| `sys_ec` | 1085 | 648 | 59.72 |
| `fwater_ec` | 1085 | 9 | 0.83 |

`fwater_ec` has a significantly lower percentage of normal readings primarily because values below 1000 are flagged as `low-ec-to-verify`, even if they are typical for freshwater. This highlights the importance of understanding the context of "normal" for different metrics.

### Recommendations

To address the issues identified and improve future crop performance, the following actions are recommended:

-   **Investigate the EC Drop:** Conduct a thorough investigation to determine the root cause of the EC drop on 2025-02-16. This should include checking for equipment malfunctions, errors in nutrient preparation, or problems with the water supply.
-   **Stabilize Environmental Controls:** Implement stricter protocols for monitoring and maintaining stable EC and pH levels. This should include regular calibration and maintenance of all sensors.
-   **Improve Data Logging Practices:** Enhance data logging procedures to ensure data completeness and accuracy. Implement automated alerts to flag anomalous readings for immediate investigation. 