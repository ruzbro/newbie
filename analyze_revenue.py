import pandas as pd

# Load the dataset
df = pd.read_csv('data/Revenue by Greenhouse by Crop.csv')

# Filter for GH3
gh3_df = df[df['resource_tag'] == 'GH3'].copy()

# Calculate total revenue
gh3_df['total_harvest_revenue'] = gh3_df['b2b_b_harvest_revenue'] + gh3_df['hotel_b_harvest_revenue']

# Group by crop and calculate metrics
crop_analysis = gh3_df.groupby('crop_name').agg(
    total_kg_harvested=('kg_harvested', 'sum'),
    average_unit_weight_g=('harvest_unit_g', 'mean'),
    total_revenue=('total_harvest_revenue', 'sum')
).reset_index()

# Sort to find highest and lowest performers
highest_kg = crop_analysis.sort_values(by='total_kg_harvested', ascending=False)
lowest_kg = crop_analysis.sort_values(by='total_kg_harvested', ascending=True)

highest_unit_weight = crop_analysis.sort_values(by='average_unit_weight_g', ascending=False)
lowest_unit_weight = crop_analysis.sort_values(by='average_unit_weight_g', ascending=True)

highest_revenue = crop_analysis.sort_values(by='total_revenue', ascending=False)
lowest_revenue = crop_analysis.sort_values(by='total_revenue', ascending=True)

print("Analysis for Greenhouse GH3:")
print("\n--- Highest performers ---")
print("\nBy Total KG Harvested:")
print(highest_kg.head().to_string())
print("\nBy Average Unit Weight (g):")
print(highest_unit_weight.head().to_string())
print("\nBy Total Revenue:")
print(highest_revenue.head().to_string())

print("\n--- Lowest performers ---")
print("\nBy Total KG Harvested:")
print(lowest_kg.head().to_string())
print("\nBy Average Unit Weight (g):")
print(lowest_unit_weight.head().to_string())
print("\nBy Total Revenue:")
print(lowest_revenue.head().to_string()) 