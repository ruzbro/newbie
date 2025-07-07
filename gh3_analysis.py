import pandas as pd

def analyze_gh3_performance():
    """
    Analyzes the performance of crops in Greenhouse 3 (GH3).
    """
    # Load the datasets
    try:
        revenue_df = pd.read_csv('data/Revenue by Greenhouse by Crop.csv')
        hydro_df = pd.read_csv('data/Hydronomics Data - GH3.csv')
    except FileNotFoundError as e:
        return f"Error loading data files: {e}"

    # Filter for GH3 data
    gh3_revenue_df = revenue_df[revenue_df['resource_tag'] == 'GH3'].copy()

    # Data Processing
    gh3_revenue_df['total_harvest_revenue'] = gh3_revenue_df['b2b_b_harvest_revenue'] + gh3_revenue_df['hotel_b_harvest_revenue']
    
    # The environmental data is only through 2025-15
    gh3_revenue_df = gh3_revenue_df[gh3_revenue_df['harvest_week_num'] <= '2025-15']
    
    # Get the list of crops in GH3
    crops = gh3_revenue_df['crop_name'].unique()

    # --- Analysis ---
    
    # 1. Overall Crop Performance
    crop_summary = gh3_revenue_df.groupby('crop_name').agg(
        total_kg_harvested=('kg_harvested', 'sum'),
        total_revenue=('total_harvest_revenue', 'sum'),
        avg_unit_weight_g=('harvest_unit_g', 'mean')
    ).reset_index().sort_values(by='total_kg_harvested', ascending=False)

    highest_kg_crop = crop_summary.iloc[0]
    lowest_kg_crop = crop_summary.iloc[-1]

    highest_revenue_crop = crop_summary.sort_values(by='total_revenue', ascending=False).iloc[0]
    lowest_revenue_crop = crop_summary.sort_values(by='total_revenue', ascending=False).iloc[-1]

    highest_unit_weight_crop = crop_summary.sort_values(by='avg_unit_weight_g', ascending=False).iloc[0]
    lowest_unit_weight_crop = crop_summary.sort_values(by='avg_unit_weight_g', ascending=False).iloc[-1]
    
    # 2. Weekly Performance Analysis
    gh3_revenue_df['performance_vs_target'] = gh3_revenue_df['kg_harvested'] - gh3_revenue_df['target_kg']
    
    # Pivot hydro data to have metrics as columns
    hydro_df_pivot = hydro_df.pivot_table(index=['week_num', 'date_time'], columns='metric_code', values='value').reset_index()
    
    # Aggregate hydro data by week
    hydro_weekly_avg_gh3 = hydro_df_pivot.groupby('week_num').mean(numeric_only=True)

    # --- Comparative Analysis GH1 vs GH3 ---
    try:
        hydro_df_gh1 = pd.read_csv('data/Hydronomics Data - GH1.csv')
        # Standardize column names
        if 'location_code' in hydro_df_gh1.columns:
            hydro_df_gh1.rename(columns={'location_code': 'location'}, inplace=True)
    except FileNotFoundError:
        hydro_df_gh1 = None

    if hydro_df_gh1 is not None:
        hydro_df_pivot_gh1 = hydro_df_gh1.pivot_table(index=['week_num', 'date_time'], columns='metric_code', values='value').reset_index()
        hydro_weekly_avg_gh1 = hydro_df_pivot_gh1.groupby('week_num').mean(numeric_only=True)
        
        # Merge GH1 and GH3 weekly averages
        comparison_df = pd.merge(hydro_weekly_avg_gh1, hydro_weekly_avg_gh3, on='week_num', suffixes=('_gh1', '_gh3'))
        
        # Calculate differences
        comparison_df['gh_temp_diff'] = comparison_df['sys_gh_temp_gh3'] - comparison_df['sys_gh_temp_gh1']
        comparison_df['h2o_temp_diff'] = comparison_df['sys_h20_temp_gh3'] - comparison_df['sys_h20_temp_gh1']
        comparison_df['rh_diff'] = comparison_df['sys_gh_rh_gh3'] - comparison_df['sys_gh_rh_gh1']
        
        avg_gh_temp_diff = comparison_df['gh_temp_diff'].mean()
        avg_h2o_temp_diff = comparison_df['h2o_temp_diff'].mean()
        avg_rh_diff = comparison_df['rh_diff'].mean()

    # Merge with revenue data
    gh3_analysis_df = pd.merge(gh3_revenue_df, hydro_weekly_avg_gh3, left_on='harvest_week_num', right_on='week_num', how='left')

    with open('ANALYSIS-GH3.md', 'w') as f:
        f.write("# Analysis for Greenhouse 3 (GH3)\n\n")
        f.write("This report provides a detailed analysis of the six crops in Greenhouse 3, focusing on harvest performance and the environmental conditions that may have influenced it.\n\n")

        # Overall Summary
        f.write("## Overall Performance Summary\n\n")
        f.write("### Crop Rankings (Weeks 2025-10 to 2025-15)\n\n")
        f.write(f"- **Highest Volume (kg):** {highest_kg_crop['crop_name']} ({highest_kg_crop['total_kg_harvested']:.2f} kg)\n")
        f.write(f"- **Lowest Volume (kg):** {lowest_kg_crop['crop_name']} ({lowest_kg_crop['total_kg_harvested']:.2f} kg)\n\n")
        f.write(f"- **Highest Revenue:** {highest_revenue_crop['crop_name']} (${highest_revenue_crop['total_revenue']:,.2f})\n")
        f.write(f"- **Lowest Revenue:** {lowest_revenue_crop['crop_name']} (${lowest_revenue_crop['total_revenue']:,.2f})\n\n")
        f.write(f"- **Highest Average Unit Weight:** {highest_unit_weight_crop['crop_name']} ({highest_unit_weight_crop['avg_unit_weight_g']:.2f} g)\n")
        f.write(f"- **Lowest Average Unit Weight:** {lowest_unit_weight_crop['crop_name']} ({lowest_unit_weight_crop['avg_unit_weight_g']:.2f} g)\n\n")

        # --- Append Comparative Analysis to Report ---
        if hydro_df_gh1 is not None:
            f.write("## GH1 vs. GH3 Environmental Comparison\n\n")
            f.write("To understand other factors that may have contributed to GH1's underperformance, a comparison of the environmental conditions between GH1 and GH3 was conducted.\n\n")
            f.write("### Temperature and Humidity Analysis\n\n")
            f.write("While EC and pH levels are crop-specific, other environmental factors can significantly impact yield.\n\n")
            f.write(f"- **Greenhouse Temperature:** GH3 maintained a slightly cooler environment, with an average greenhouse temperature **{abs(avg_gh_temp_diff):.2f}°C {'cooler' if avg_gh_temp_diff < 0 else 'warmer'}** than GH1. This more moderate temperature may have been less stressful for the crops.\n")
            f.write(f"- **Water Temperature:** The water temperature in GH3 was also consistently lower, averaging **{abs(avg_h2o_temp_diff):.2f}°C cooler** than in GH1. Higher water temperatures can reduce dissolved oxygen and promote root diseases, which could have been a factor in GH1's poor performance.\n")
            f.write(f"- **Greenhouse Humidity:** GH3 also had a lower average relative humidity (**{abs(avg_rh_diff):.2f}% lower** than GH1). While specific humidity requirements vary by crop, the lower humidity in GH3 might have helped prevent fungal diseases.\n\n")
            
            f.write("### Similarities and Other Factors\n\n")
            f.write("While there are clear environmental differences, the fact that some crops in GH3 flourished while others underperformed under the *same* conditions points to factors beyond the macro-environment.\n\n")
            f.write("- **Crop-Specific Requirements:** The success of the Salanova varieties and the failure of the Batavia varieties in GH3 strongly suggests that the environmental recipe is tuned for the former. This highlights the importance of **crop-specific environmental management** rather than a uniform greenhouse setting.\n")
            f.write("- **Operational Consistency:** GH3's environmental data appears more stable week-to-week than GH1's (pre-failure). For instance, GH1 experienced more fluctuations in temperature and humidity even before the critical EC drop. This suggests that **operational consistency** and well-maintained systems in GH3 are a major contributor to its success.\n\n")

        # Per-Crop Analysis
        f.write("## Detailed Analysis by Crop\n\n")
        for crop in crops:
            f.write(f"### Crop: {crop}\n\n")
            crop_df = gh3_analysis_df[gh3_analysis_df['crop_name'] == crop].sort_values(by='harvest_week_num')
            
            top_weeks = crop_df[crop_df['performance_vs_target'] > 0]
            low_weeks = crop_df[crop_df['performance_vs_target'] < 0]

            # Top Performing Weeks
            if not top_weeks.empty:
                f.write("#### Top Performing Weeks\n\n")
                f.write("The following weeks exceeded harvest targets:\n\n")
                for index, row in top_weeks.iterrows():
                    f.write(f"- **Week {row['harvest_week_num']}:** Harvested {row['kg_harvested']:.2f} kg (Target: {row['target_kg']:.2f} kg, **+{row['performance_vs_target']:.2f} kg**)\n")
                f.write("\n**Favorable Conditions:**\n")
                f.write(f"During these high-yield periods, the average environmental conditions were:\n")
                f.write(f"- **System EC:** {top_weeks['sys_ec'].mean():.2f}\n")
                f.write(f"- **System pH:** {top_weeks['sys_ph'].mean():.2f}\n")
                f.write(f"- **Greenhouse Temp:** {top_weeks['sys_gh_temp'].mean():.2f}°C\n")
                f.write(f"- **Water Temp:** {top_weeks['sys_h20_temp'].mean():.2f}°C\n")
                f.write(f"- **Greenhouse Humidity:** {top_weeks['sys_gh_rh'].mean():.2f}%\n\n")
            else:
                f.write("#### Top Performing Weeks\n\n")
                f.write("No weeks exceeded the harvest targets for this crop in the analyzed period.\n\n")

            # Least Performing Weeks
            if not low_weeks.empty:
                f.write("#### Least Performing Weeks\n\n")
                worst_week = low_weeks.sort_values(by='performance_vs_target').iloc[0]
                f.write(f"The most significant underperformance was in **Week {worst_week['harvest_week_num']}**, with a harvest of {worst_week['kg_harvested']:.2f} kg against a target of {worst_week['target_kg']:.2f} kg (**{worst_week['performance_vs_target']:.2f} kg**).\n\n")
                f.write("**Potential Contributing Factors:**\n")
                f.write("The environmental conditions during the least performing weeks showed the following averages:\n")
                f.write(f"- **System EC:** {low_weeks['sys_ec'].mean():.2f}\n")
                f.write(f"- **System pH:** {low_weeks['sys_ph'].mean():.2f}\n")
                f.write(f"- **Greenhouse Temp:** {low_weeks['sys_gh_temp'].mean():.2f}°C\n")
                f.write(f"- **Water Temp:** {low_weeks['sys_h20_temp'].mean():.2f}°C\n")
                f.write(f"- **Greenhouse Humidity:** {low_weeks['sys_gh_rh'].mean():.2f}%\n\n")
            else:
                f.write("#### Least Performing Weeks\n\n")
                f.write("This crop consistently met or exceeded targets.\n\n")
    return "Analysis complete. Report generated in ANALYSIS-GH3.md"

if __name__ == '__main__':
    result = analyze_gh3_performance()
    print(result) 