import pandas as pd

# Load the datasets
revenue_df = pd.read_csv('data/Revenue by Greenhouse by Crop.csv')
crop_calendar_df = pd.read_csv('data/crop calendar weeks 2025-08 to 2025-32.csv')
hydroponics_df = pd.read_csv('data/Hydronomics Data gh1gh3.csv')

# Clean up resource_tag in crop_calendar
crop_calendar_df['resource_tag'] = crop_calendar_df['resource_tag'].str.replace('PNQ-', '')

# Convert date columns to datetime objects
crop_calendar_df['seeding_date'] = pd.to_datetime(crop_calendar_df['seeding_date']).dt.tz_localize(None)
crop_calendar_df['transplant_date'] = pd.to_datetime(crop_calendar_df['transplant_date']).dt.tz_localize(None)
crop_calendar_df['harvest_date'] = pd.to_datetime(crop_calendar_df['harvest_date']).dt.tz_localize(None)
hydroponics_df['date_time'] = pd.to_datetime(hydroponics_df['date_time'])
hydroponics_df['value'] = pd.to_numeric(hydroponics_df['value'], errors='coerce')


# Filter for least performing weeks in GH3 (mid-April to end of May)
# Week numbers for this period are approximately 16 to 22
least_performing_df = revenue_df[
    (revenue_df['resource_tag'] == 'GH3') &
    (revenue_df['harvest_week_num'].str[5:].astype(int) >= 16) &
    (revenue_df['harvest_week_num'].str[5:].astype(int) <= 22) &
    (revenue_df['pct_of_target_kg'] < -10)
].copy()

# Merge with crop calendar to get cycle dates
bottom_weeks_analysis = pd.merge(
    least_performing_df,
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

# Analyze conditions for each least performing crop harvest
results = []
for index, row in bottom_weeks_analysis.iterrows():
    seeding_date = row['seeding_date']
    transplant_date = row['transplant_date']
    harvest_date = row['harvest_date']
    greenhouse = row['resource_tag']
    crop_name = row['crop_name']
    harvest_week_num = row['harvest_week_num']
    
    # Nursery conditions
    nursery_ec = get_avg_hydroponics(seeding_date, transplant_date, greenhouse, 'sys_ec')
    nursery_ph = get_avg_hydroponics(seeding_date, transplant_date, greenhouse, 'sys_ph')
    nursery_temp = get_avg_hydroponics(seeding_date, transplant_date, greenhouse, 'sys_h20_temp')
    
    # Growing conditions
    growing_ec = get_avg_hydroponics(transplant_date, harvest_date, greenhouse, 'sys_ec')
    growing_ph = get_avg_hydroponics(transplant_date, harvest_date, greenhouse, 'sys_ph')
    growing_temp = get_avg_hydroponics(transplant_date, harvest_date, greenhouse, 'sys_h20_temp')
    
    results.append({
        'harvest_week': harvest_week_num,
        'crop': crop_name,
        'pct_target_kg': row['pct_of_target_kg'],
        'nursery_avg_ec': nursery_ec,
        'nursery_avg_ph': nursery_ph,
        'nursery_avg_temp': nursery_temp,
        'growing_avg_ec': growing_ec,
        'growing_avg_ph': growing_ph,
        'growing_avg_temp': growing_temp
    })

results_df = pd.DataFrame(results).drop_duplicates()
print("Analysis of conditions for least performing weeks in GH3 (mid-April to end of May):")
print(results_df.to_string()) 