import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Load the dataset
try:
    df = pd.read_csv('data/Revenue by Greenhouse by Crop.csv')
except FileNotFoundError:
    print("Error: The file 'data/Revenue by Greenhouse by Crop.csv' was not found.")
    exit()

# Data cleaning: 'kg_harvested' might have non-numeric values. Coerce errors will turn them into NaN
df['kg_harvested'] = pd.to_numeric(df['kg_harvested'], errors='coerce')
# Drop rows where kg_harvested is NaN after coercion, if any
df.dropna(subset=['kg_harvested'], inplace=True)

# --- Filter out future harvest dates ---
# Assuming 'current_week' column is consistent, take the first value as the reference
current_week = df['current_week'].iloc[0]
df_filtered = df[df['harvest_week_num'] <= current_week].copy()

# --- Analysis 1: Total kg_harvested by greenhouse over time (filtered) ---

# Group by week and greenhouse to sum harvested kg from the filtered data
weekly_harvest = df_filtered.groupby(['harvest_week_num', 'resource_tag'])['kg_harvested'].sum().unstack().fillna(0)

# Sort by harvest week
weekly_harvest.sort_index(inplace=True)

# Create a mapping from harvest_week_num to week_label for plot labels using the filtered data
week_labels = df_filtered.drop_duplicates(subset='harvest_week_num').set_index('harvest_week_num')['week_label'].sort_index()

# Plotting
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(15, 8))

weekly_harvest.plot(kind='line', ax=ax, marker='o')

# Formatting the plot
ax.set_title('Total kg Harvested by Greenhouse per Week', fontsize=16, fontweight='bold')
ax.set_xlabel('Harvest Week', fontsize=12)
ax.set_ylabel('Total Kilograms Harvested', fontsize=12)
ax.legend(title='Greenhouse')
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Set x-axis labels
tick_locations = range(len(weekly_harvest.index))
ax.set_xticks(tick_locations)
# Ensure the labels align with the sorted weekly_harvest index
ax.set_xticklabels(week_labels.reindex(weekly_harvest.index).values, rotation=45, ha='right')


# Make sure all labels are shown
fig.tight_layout()

# Save the plot
plot_filename = './analysis/charts/greenhouse_weekly_harvest_past_only.png'
plt.savefig(plot_filename)
print(f"Plot saved to {plot_filename}")


# --- Analysis 2: Which greenhouse performed best overall (filtered) ---
total_harvest_by_gh = df_filtered.groupby('resource_tag')['kg_harvested'].sum().sort_values(ascending=False)

print("\nTotal Kilograms Harvested by Greenhouse (Up to Current Week):")
print(total_harvest_by_gh)

best_gh = total_harvest_by_gh.index[0]
best_gh_value = total_harvest_by_gh.iloc[0]

print(f"\nConclusion:")
print(f"Based on the total kilograms harvested up to the current week, {best_gh} was the best performing greenhouse, with a total of {best_gh_value:.2f} kg harvested.") 