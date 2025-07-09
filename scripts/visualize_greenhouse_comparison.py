import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visualize_greenhouse_comparison(
    input_csv_path: str,
    locations_to_plot: list,
    metrics_to_plot: list,
    output_html_path: str = "greenhouse_comparison.html",
    title: str = "Environmental Metrics Comparison"
):
    """
    Generates a Plotly visualization comparing environmental metrics
    across specified locations.

    Args:
        input_csv_path (str): Path to the input CSV file (e.g., 'data/Hydronomics Data Combined.csv').
        locations_to_plot (list): List of location strings to include in the plot (e.g., ['GH1', 'GH3']).
        metrics_to_plot (list): List of metric codes to plot (e.g., ['sys_gh_temp', 'sys_gh_rh']).
        output_html_path (str): Path to save the output HTML file.
        title (str): Title of the overall plot.
    """
    try:
        env_data = pd.read_csv(input_csv_path)
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return

    # --- Data Cleaning ---
    env_data['value'] = pd.to_numeric(env_data['value'], errors='coerce')
    env_data['date_time'] = pd.to_datetime(env_data['date_time'])
    
    # Remove known anomalous values (can be customized or removed if not needed for all datasets)
    env_data = env_data[~((env_data['metric_code'] == 'sys_ph') & (env_data['value'] < 4))]
    env_data = env_data[~((env_data['metric_code'] == 'sys_gh_temp') & (env_data['value'] < 10))]

    # --- Data Preparation ---
    plot_data = env_data[
        env_data['metric_code'].isin(metrics_to_plot) &
        env_data['location'].isin(locations_to_plot)
    ]

    # --- Visualization ---
    fig = make_subplots(
        rows=len(metrics_to_plot), 
        cols=1, 
        subplot_titles=[f'{metric} Comparison' for metric in metrics_to_plot],
        shared_xaxes=True
    )

    colors = {'GH1': 'blue', 'GH2': 'green', 'GH3': 'red', 'GH4': 'purple', 'NURSERY': 'orange'}

    for i, metric in enumerate(metrics_to_plot, 1):
        for location in locations_to_plot:
            metric_data = plot_data[
                (plot_data['metric_code'] == metric) &
                (plot_data['location'] == location)
            ].sort_values('date_time')

            fig.add_trace(
                go.Scatter(
                    x=metric_data['date_time'], 
                    y=metric_data['value'], 
                    name=f'{location} - {metric}', 
                    mode='lines',
                    line=dict(color=colors.get(location, 'black'))
                ),
                row=i, col=1
            )
        fig.update_yaxes(title_text=metric, row=i, col=1)

    fig.update_layout(
        height=400 * len(metrics_to_plot), 
        width=1000, 
        title_text=title,
        hovermode="x unified"
    )

    # Save to HTML
    fig.write_html(output_html_path)
    print(f"Visualization saved to {output_html_path}")

if __name__ == "__main__":
    # Example 1: Visualize Combined Data (GH1, GH2, GH3, GH4)
    print("Generating visualization for Combined Data...")
    visualize_greenhouse_comparison(
        input_csv_path='data/Hydronomics Data Combined.csv',
        locations_to_plot=['GH1', 'GH2', 'GH3', 'GH4'],
        metrics_to_plot=['sys_gh_temp', 'sys_gh_rh', 'sys_h20_temp', 'fwater_temp'],
        output_html_path="./analysis/charts/greenhouse_combined_comparison.html",
        title="All Greenhouses Environmental Comparison"
    )

    # Example 2: Visualize Nursery Data
    print("\nGenerating visualization for Nursery Data...")
    visualize_greenhouse_comparison(
        input_csv_path='data/Hydronomics Data nursery.csv',
        locations_to_plot=['NURSERY'],
        metrics_to_plot=['sys_gh_temp', 'sys_gh_rh', 'sys_h20_temp', 'fwater_temp'], # Assuming these metrics exist for Nursery
        output_html_path="./analysis/charts/greenhouse_nursery_comparison.html",
        title="Nursery Environmental Comparison"
    )