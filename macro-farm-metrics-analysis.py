import pandas as pd
import numpy as np

def analyze_temperature_patterns(target_greenhouses=None, target_metrics=None):
    """
    Analyzes weekly median temperature data from the Hydronomics dataset to find
    patterns and identify greenhouses with the highest and lowest values.

    Args:
        target_greenhouses (list, optional): A list of greenhouse locations to analyze. 
                                            Defaults to all available greenhouses.
        target_metrics (list, optional): A list of metric codes to analyze. 
                                         Defaults to all temperature-related metrics.
    """
    # --- 1. Load and Prepare Data ---
    try:
        df = pd.read_csv('data/Hydronomics Data Merged.csv')
    except FileNotFoundError:
        print("Error: 'data/Hydronomics Data Merged.csv' not found.")
        return

    # --- 2. Clean and Process Data ---
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # Filter for clean, non-zero data
    df_clean = df[(df['status'].isnull()) & (df['value'] != 0)].copy()

    # --- 3. Filter by Parameters ---
    # Default to all temp metrics if none are specified
    if target_metrics is None:
        target_metrics = ['sys_gh_temp', 'sys_h20_temp', 'fwater_temp']
    
    df_filtered = df_clean[df_clean['metric_code'].isin(target_metrics)]

    if target_greenhouses:
        df_filtered = df_filtered[df_filtered['location'].isin(target_greenhouses)]

    if df_filtered.empty:
        print("No data available for the specified filters.")
        return

    # --- 4. Perform Weekly Median Analysis ---
    df_filtered['week'] = df_filtered['date_time'].dt.strftime('%Y-%U')
    
    weekly_medians = df_filtered.groupby(['week', 'location', 'metric_code'])['value'].median().reset_index()
    
    print("--- Weekly Temperature Analysis ---")

    for metric in target_metrics:
        metric_df = weekly_medians[weekly_medians['metric_code'] == metric]
        if metric_df.empty:
            continue

        print(f"\n--- Analysis for Metric: {metric} ---")

        # Find overall highest and lowest weekly median
        highest_week = metric_df.loc[metric_df['value'].idxmax()]
        lowest_week = metric_df.loc[metric_df['value'].idxmin()]
        
        print(f"Highest Median Reading: {highest_week['value']:.2f} in {highest_week['location']} during week {highest_week['week']}")
        print(f"Lowest Median Reading:  {lowest_week['value']:.2f} in {lowest_week['location']} during week {lowest_week['week']}")

        # --- 5. Analyze Patterns Between Greenhouses ---
        # Pivot to compare greenhouses side-by-side
        pivot_df = metric_df.pivot(index='week', columns='location', values='value')
        
        # Get pairs of greenhouses to compare
        locations = pivot_df.columns.tolist()
        compared_pairs = set()
        
        print("\nAverage Temperature Differences:")
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                loc1 = locations[i]
                loc2 = locations[j]
                
                # Calculate the difference, ignoring weeks where one has no data
                diff = (pivot_df[loc1] - pivot_df[loc2]).dropna()
                
                if diff.empty:
                    continue
                    
                avg_diff = diff.mean()
                print(f"- {loc1} vs {loc2}: {loc1} is on average {avg_diff:.2f}°C {'higher' if avg_diff > 0 else 'lower'} than {loc2}")

# --- Main execution block ---
if __name__ == "__main__":
    print("Running analysis for all greenhouses and default temperature metrics...")
    # Example: Run with default parameters (all greenhouses, all temp metrics)
    analyze_temperature_patterns()
    
    # Example: Run with specific parameters
    # print("\n\nRunning analysis for specific greenhouses and metrics...")
    # analyze_temperature_patterns(target_greenhouses=['GH1', 'GH3'], target_metrics=['sys_gh_temp'])
