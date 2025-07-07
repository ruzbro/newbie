import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visualize_greenhouse_comparison():
    """
    Generates a Plotly visualization comparing environmental metrics
    between Greenhouse 1 and Greenhouse 3.
    """
    try:
        env_data = pd.read_csv('data/gh1gh3.csv')
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return

    # --- Data Cleaning ---
    env_data['value'] = pd.to_numeric(env_data['value'], errors='coerce')
    env_data['date_time'] = pd.to_datetime(env_data['date_time'])
    
    # Remove known anomalous values
    env_data = env_data[~((env_data['metric_code'] == 'sys_ph') & (env_data['value'] < 4))]
    env_data = env_data[~((env_data['metric_code'] == 'sys_gh_temp') & (env_data['value'] < 10))]

    # --- Data Preparation ---
    metrics_to_plot = ['sys_gh_temp', 'sys_gh_rh', 'sys_h20_temp', 'fwater_temp']
    
    # Filter for the metrics we want to plot
    plot_data = env_data[env_data['metric_code'].isin(metrics_to_plot)]

    gh1_data = plot_data[plot_data['location'] == 'GH1']
    gh3_data = plot_data[plot_data['location'] == 'GH3']

    # --- Visualization ---
    fig = make_subplots(
        rows=len(metrics_to_plot), 
        cols=1, 
        subplot_titles=[f'{metric} Comparison' for metric in metrics_to_plot]
    )

    for i, metric in enumerate(metrics_to_plot, 1):
        gh1_metric_data = gh1_data[gh1_data['metric_code'] == metric].sort_values('date_time')
        gh3_metric_data = gh3_data[gh3_data['metric_code'] == metric].sort_values('date_time')

        fig.add_trace(
            go.Scatter(
                x=gh1_metric_data['date_time'], 
                y=gh1_metric_data['value'], 
                name='GH1', 
                mode='lines',
                line=dict(color='blue')
            ),
            row=i, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=gh3_metric_data['date_time'], 
                y=gh3_metric_data['value'], 
                name='GH3', 
                mode='lines',
                line=dict(color='red')
            ),
            row=i, col=1
        )
        fig.update_yaxes(title_text=metric, row=i, col=1)

    fig.update_layout(
        height=1200, 
        width=900, 
        title_text="Greenhouse 1 vs. Greenhouse 3 Environmental Comparison"
    )

    # Save to HTML
    fig.write_html("greenhouse_comparison.html")
    print("Visualization saved to greenhouse_comparison.html")

if __name__ == "__main__":
    visualize_greenhouse_comparison() 