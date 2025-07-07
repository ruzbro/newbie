import pandas as pd

# Load the revenue data
revenue_df = pd.read_csv('data/Revenue by Greenhouse by Crop.csv')

# Filter for GH3 and top performing weeks
top_weeks_df = revenue_df[
    (revenue_df['resource_tag'] == 'GH3') &
    (revenue_df['pct_of_target_kg'] > 0)
].copy()

print("Top performing weeks in GH3 (where kg harvested > target):")
print(top_weeks_df[['harvest_week_num', 'crop_name', 'kg_harvested', 'target_kg', 'pct_of_target_kg']].to_string()) 