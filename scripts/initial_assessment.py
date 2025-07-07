import pandas as pd

def assess_data_veracity():
    """
    Performs an initial assessment of the greenhouse data.
    - Loads environmental and revenue data.
    - Checks for data quality issues.
    - Compares key environmental metrics between GH1 and GH3.
    """
    # Load the datasets
    try:
        env_data = pd.read_csv('data/gh1gh3.csv')
        revenue_data = pd.read_csv('data/Revenue by Greenhouse by Crop.csv')
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return

    # Convert 'value' column to numeric, coercing errors to NaN
    env_data['value'] = pd.to_numeric(env_data['value'], errors='coerce')

    print("--- Data Veracity Check ---")
    print("\nEnvironmental Data Info:")
    env_data.info()
    print("\nRevenue Data Info:")
    revenue_data.info()

    print("\nEnvironmental Data Description:")
    print(env_data.describe())

    print("\nRevenue Data Description:")
    print(revenue_data.describe())

    print("\n--- Greenhouse Comparison (Environmental) ---")
    
    # Filter data for each greenhouse
    gh1_env = env_data[env_data['location'] == 'GH1']
    gh3_env = env_data[env_data['location'] == 'GH3']

    # Metrics to compare
    metrics_to_compare = ['sys_gh_temp', 'sys_gh_rh', 'sys_ec', 'sys_ph']

    for metric in metrics_to_compare:
        print(f"\n--- Comparison for {metric} ---")
        
        gh1_metric = gh1_env[gh1_env['metric_code'] == metric]['value']
        gh3_metric = gh3_env[gh3_env['metric_code'] == metric]['value']
        
        print("\nGreenhouse 1:")
        print(gh1_metric.describe())
        
        print("\nGreenhouse 3:")
        print(gh3_metric.describe())

        # Check for significant difference
        if gh1_metric.mean() > gh3_metric.mean():
            diff = gh1_metric.mean() - gh3_metric.mean()
            print(f"\nOn average, GH1's {metric} is {diff:.2f} higher than GH3's.")
        else:
            diff = gh3_metric.mean() - gh1_metric.mean()
            print(f"\nOn average, GH3's {metric} is {diff:.2f} higher than GH1's.")


if __name__ == "__main__":
    assess_data_veracity() 