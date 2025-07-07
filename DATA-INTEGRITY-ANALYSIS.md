# Data Integrity Analysis

This document summarizes the findings from the initial data integrity assessment of the greenhouse environmental data (`gh1gh3.csv`) and revenue data (`Revenue by Greenhouse by Crop.csv`).

## Environmental Data (`gh1gh3.csv`)

### Data Quality Issues

1.  **Missing Values:** The dataset contains a significant number of missing values in the `value` column. Approximately **19%** of the environmental readings are missing, which can affect the accuracy of any time-series analysis or aggregation.

2.  **Incorrect Data Type:** The `value` column, which contains all sensor readings, was initially read as a text (object) type instead of a numeric type. This was corrected by converting the column to a numeric type during analysis, but it points to a potential issue in the data export or logging process.

3.  **Anomalous Readings:** Several extreme and unrealistic values were identified, which are likely data-entry errors. These outliers can skew statistical analysis and should be filtered out before performing any detailed analysis.

### Erroneous Readings Identified

The following anomalous values were found in the environmental data for Greenhouse 3:

*   **System pH (`sys_ph`):** A minimum pH of **0.98** was recorded. This is chemically implausible for a hydroponic system, where pH is typically maintained between 5.5 and 6.5.
*   **Greenhouse Temperature (`sys_gh_temp`):** A minimum temperature of **3.3°C** was recorded. This is far too cold for the crops grown in this greenhouse and is likely an error from a malfunctioning sensor or incorrect data entry.

These values were identified in Greenhouse 3's data and were not present in Greenhouse 1's data, which suggests a potential issue specific to GH3's monitoring equipment or data logging procedures.

## Revenue Data (`Revenue by Greenhouse by Crop.csv`)

The revenue and harvest dataset is largely complete and appears to be reliable. Only a few missing data points were noted for `harvest_unit_g`, which are minor and unlikely to have a significant impact on the overall analysis.

## Recommendations

-   **Investigate Missing Data:** The root cause of the missing environmental data should be investigated. This may involve checking the data logging equipment, network connectivity, and data processing pipeline.
-   **Implement Data Validation:** A data validation layer should be added to the data ingestion process to automatically flag or reject anomalous values that fall outside of realistic operational ranges.
-   **Review GH3's Sensors:** The sensors in Greenhouse 3 should be calibrated and checked for malfunctions to prevent future erroneous readings. 