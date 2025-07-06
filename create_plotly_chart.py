import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pcolors

# --- 1. Load and Prepare the Data ---
try:
    df = pd.read_csv('data/Revenue by Greenhouse by Crop.csv')
except FileNotFoundError:
    print("Error: The file 'data/Revenue by Greenhouse by Crop.csv' was not found.")
    exit()

# Data cleaning and filtering
df['kg_harvested'] = pd.to_numeric(df['kg_harvested'], errors='coerce')
df.dropna(subset=['kg_harvested'], inplace=True)

# Filter out future harvest dates
current_week = df['current_week'].iloc[0]
df_filtered = df[df['harvest_week_num'] <= current_week].copy()

# --- 2. Determine Stacking Order ---
# Calculate total harvest to determine the stacking order (highest to lowest)
total_harvest_by_gh = df_filtered.groupby('resource_tag')['kg_harvested'].sum().sort_values(ascending=False)
stacking_order = total_harvest_by_gh.index.tolist() # GH3, GH4, GH2, GH1

# --- 3. Pivot Data for Plotting ---
# Group by week and greenhouse, then pivot
weekly_harvest = df_filtered.groupby(['harvest_week_num', 'resource_tag', 'week_label'])['kg_harvested'].sum().unstack(level='resource_tag').fillna(0)
weekly_harvest.sort_index(inplace=True)

# Extract week labels for the x-axis
week_labels = weekly_harvest.index.get_level_values('week_label')

# --- 4. Create the Plotly Stacked Area Chart ---
fig = go.Figure()

# Define a pastel color palette
pastel_colors = pcolors.qualitative.Pastel

# Add traces in the desired stacking order
for i, gh in enumerate(stacking_order):
    fig.add_trace(go.Scatter(
        x=week_labels, 
        y=weekly_harvest[gh],
        name=gh,
        mode='lines',
        line=dict(width=0.5, color=pastel_colors[i]),
        stackgroup='one', # Creates the stacked area chart
        hoverinfo='x+y',
        hovertemplate=f'<b>{gh}</b><br>' + 
                      '%{x}<br>' +
                      'Harvested: %{y:.2f} kg<extra></extra>'
    ))

# --- 5. Customize the Layout ---
fig.update_layout(
    title='Total kg Harvested by Greenhouse per Week (Stacked)',
    xaxis_title='Harvest Week',
    yaxis_title='Total Kilograms Harvested',
    legend=dict(
        x=0.01,
        y=0.99,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.6)' # Semi-transparent background
    ),
    hovermode='x unified',
    template='plotly_white'
)

# Customize x-axis tick rotation
fig.update_xaxes(tickangle=45)

# --- 6. Save as HTML ---
output_filename = 'greenhouse_harvest_stacked_area.html'
fig.write_html(output_filename)

print(f"Interactive plot saved to {output_filename}") 