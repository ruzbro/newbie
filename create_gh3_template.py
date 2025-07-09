
import pandas as pd
import numpy as np

def create_gh3_template():
    gh4_template_path = "/workspaces/newbie/data/GH4 Template - data gh4.csv"
    gh3_template_output_path = "/workspaces/newbie/data/GH3 Template - data gh3.csv"

    try:
        # Read the GH4 template
        gh4_template_df = pd.read_csv(gh4_template_path)

        # Select the first three columns
        gh3_template_df = gh4_template_df[['metric_code', 'date_time', 'week_num']].copy()

        # Add an empty 'value' column
        gh3_template_df['value'] = np.nan

        # Set the 'location' column to 'GH3'
        gh3_template_df['location'] = 'GH3'

        # Save the new template
        gh3_template_df.to_csv(gh3_template_output_path, index=False)
        print(f"Successfully created GH3 template at {gh3_template_output_path}")

    except FileNotFoundError as e:
        print(f"Error: Template file not found - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_gh3_template()
