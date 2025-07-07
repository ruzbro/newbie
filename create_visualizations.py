import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. Load and Prepare Data ---

# Load the datasets
revenue_df = pd.read_csv('data/Revenue by Greenhouse by Crop.csv')
crop_calendar_df = pd.read_csv('data/crop calendar weeks 2025-08 to 2025-32.csv')
hydroponics_df = pd.read_csv('data/Hydronomics Data gh1gh3.csv')

# --- Clean and Process Data ---

# Clean up resource_tag in crop_calendar
crop_calendar_df['resource_tag'] = crop_calendar_df['resource_tag'].str.replace('PNQ-', '')

# Convert date columns to datetime objects and handle timezones
crop_calendar_df['seeding_date'] = pd.to_datetime(crop_calendar_df['seeding_date']).dt.tz_localize(None)
crop_calendar_df['transplant_date'] = pd.to_datetime(crop_calendar_df['transplant_date']).dt.tz_localize(None)
crop_calendar_df['harvest_date'] = pd.to_datetime(crop_calendar_df['harvest_date']).dt.tz_localize(None)
hydroponics_df['date_time'] = pd.to_datetime(hydroponics_df['date_time'])
hydroponics_df['value'] = pd.to_numeric(hydroponics_df['value'], errors='coerce')

# --- 2. Chart 1: Production Comparison During Hot Weather ---

# Filter for Romaine and Oakleaf in GH3 during the hot period (weeks 16-22)
hot_period_df = revenue_df[
    (revenue_df['resource_tag'] == 'GH3') &
    (revenue_df['harvest_week_num'].str[5:].astype(int) >= 16) &
    (revenue_df['harvest_week_num'].str[5:].astype(int) <= 22) &
    (revenue_df['crop_name'].isin(['Romaine', 'Green Salanova Oakleaf']))
].copy()

# Create the comparison chart
fig1 = go.Figure()

for crop in ['Romaine', 'Green Salanova Oakleaf']:
    crop_df = hot_period_df[hot_period_df['crop_name'] == crop]
    fig1.add_trace(go.Scatter(
        x=crop_df['harvest_week_num'],
        y=crop_df['pct_of_target_kg'],
        mode='lines+markers',
        name=crop
    ))

fig1.update_layout(
    title='Production Performance: Romaine vs. Oakleaf During Extreme Heat (Weeks 16-22)',
    xaxis_title='Harvest Week',
    yaxis_title='% of Target Kg Harvested',
    legend_title='Crop',
    template='plotly_white'
)

fig1.write_html('analysis/charts/romaine_vs_oakleaf_performance.html')
print("Chart 1 saved to analysis/charts/romaine_vs_oakleaf_performance.html")


# --- 3. Chart 2: "Perfect Storm" Analysis for Green Salanova Oakleaf ---

# Filter for Green Salanova Oakleaf in GH3
oakleaf_df = revenue_df[
    (revenue_df['resource_tag'] == 'GH3') &
    (revenue_df['crop_name'] == 'Green Salanova Oakleaf')
].copy()

# Merge with crop calendar to get cycle dates
oakleaf_analysis = pd.merge(
    oakleaf_df,
    crop_calendar_df,
    on=['crop_name', 'harvest_week_num', 'resource_tag']
)

# Function to get average hydroponics data for a given period
def get_avg_hydroponics(start_date, end_date, greenhouse, metric):
    mask = (
        (hydroponics_df['location'] == greenhouse) &
        (hydroponics_df['date_time'] >= start_date) &
        (hydroponics_df['date_time'] <= end_date) &
        (hydroponics_df['metric_code'] == metric)
    )
    return hydroponics_df[mask]['value'].mean()

# Calculate the growing conditions for each harvest week
conditions = []
for index, row in oakleaf_analysis.iterrows():
    conditions.append({
        'harvest_week': row['harvest_week_num'],
        'pct_target_kg': row['pct_of_target_kg'],
        'growing_avg_ec': get_avg_hydroponics(row['transplant_date'], row['harvest_date'], row['resource_tag'], 'sys_ec'),
        'growing_avg_ph': get_avg_hydroponics(row['transplant_date'], row['harvest_date'], row['resource_tag'], 'sys_ph'),
        'growing_avg_temp': get_avg_hydroponics(row['transplant_date'], row['harvest_date'], row['resource_tag'], 'sys_h20_temp')
    })

conditions_df = pd.DataFrame(conditions).sort_values('harvest_week')

# Create the "perfect storm" chart with multiple y-axes
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces for conditions
fig2.add_trace(go.Scatter(x=conditions_df['harvest_week'], y=conditions_df['growing_avg_temp'], name='Avg. Water Temp (°C)'), secondary_y=False)
fig2.add_trace(go.Scatter(x=conditions_df['harvest_week'], y=conditions_df['growing_avg_ph'], name='Avg. pH'), secondary_y=False)
fig2.add_trace(go.Scatter(x=conditions_df['harvest_week'], y=conditions_df['growing_avg_ec'], name='Avg. EC'), secondary_y=False)

# Add trace for performance
fig2.add_trace(go.Scatter(x=conditions_df['harvest_week'], y=conditions_df['pct_target_kg'], name='% of Target Kg', line=dict(color='red', dash='dash')), secondary_y=True)

fig2.update_layout(
    title_text='"Perfect Storm": Impact of Temp, pH, & EC on Green Salanova Oakleaf',
    template='plotly_white',
    legend_title='Metric'
)

fig2.update_xaxes(title_text='Harvest Week')
fig2.update_yaxes(title_text='Hydroponics Value (Temp, pH, EC)', secondary_y=False)
fig2.update_yaxes(title_text='% of Target Kg Harvested', secondary_y=True)

fig2.write_html('analysis/charts/perfect_storm_oakleaf.html')
print("Chart 2 saved to analysis/charts/perfect_storm_oakleaf.html") 