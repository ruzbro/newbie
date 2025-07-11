
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_plot(target_greenhouses=None, target_metrics=None):
    """
    Generates a plot of greenhouse metrics, optionally filtering by greenhouse and metric codes.
    Zero values are excluded from the plot.

    Args:
        target_greenhouses (list, optional): A list of greenhouse locations to include. Defaults to all.
        target_metrics (list, optional): A list of metric codes to include. Defaults to all.
    """
    # --- 1. Load and Prepare Data ---
    try:
        df = pd.read_csv('data/Hydronomics Data Merged.csv')
    except FileNotFoundError:
        print("Error: 'data/Hydronomics Data Merged.csv' not found.")
        return

    # --- 2. Clean and Process Data ---
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(subset=['value'], inplace=True)
    df_clean = df[df['status'].isnull()].copy()

    # --- 3. Map Metric Codes to Names ---
    METRIC_NAME_MAP = {
        'sys_ec': 'System EC',
        'fwater_ec': 'Freshwater EC',
        'sys_ph': 'System PH',
        'fwater_ph': 'Freshwater PH',
        'sys_h20_temp': 'Water Temp',
        'fwater_temp': 'Freshwater Temp',
        'sys_gh_temp': 'Greenhouse Temp',
        'sys_gh_rh': 'Greenhouse Relative Humidity'
    }

    # --- 4. Filter Data ---
    df_to_plot = df_clean.copy()
    if target_greenhouses:
        df_to_plot = df_to_plot[df_to_plot['location'].isin(target_greenhouses)]
    if target_metrics:
        df_to_plot = df_to_plot[df_to_plot['metric_code'].isin(target_metrics)]

    # --- 5. Create Visualizations ---
    metrics_to_plot = sorted(df_to_plot['metric_code'].unique())
    if not metrics_to_plot:
        print("No data to plot for the specified filters.")
        return

    subplot_titles = [METRIC_NAME_MAP.get(code, code) for code in metrics_to_plot]
    fig = make_subplots(rows=len(metrics_to_plot), cols=1, subplot_titles=subplot_titles)
    colors = {'GH1': 'blue', 'GH2': 'green', 'GH3': 'red', 'GH4': 'purple', 'Nursery': 'orange'}

    for i, metric_code in enumerate(metrics_to_plot):
        metric_df = df_to_plot[df_to_plot['metric_code'] == metric_code]
        for gh in sorted(metric_df['location'].unique()):
            gh_df = metric_df[metric_df['location'] == gh]
            
            # Exclude zero values from the trace
            gh_df = gh_df[gh_df['value'] != 0].copy()
            if gh_df.empty:
                continue

            fig.add_trace(
                go.Scatter(
                    x=gh_df['date_time'],
                    y=gh_df['value'],
                    name=gh,
                    mode='lines',
                    line=dict(color=colors.get(gh, 'black')),
                    legendgroup=gh,
                    showlegend=(i == 0)
                ),
                row=i + 1,
                col=1
            )

    # --- 6. Customize Layout and Title ---
    if not target_greenhouses and not target_metrics:
        title_text = 'Greenhouse Metrics (Clean)'
    else:
        gh_str = f"Greenhouses: {', '.join(target_greenhouses)}" if target_greenhouses else "All Greenhouses"
        metrics_str = f"Metrics: {', '.join([METRIC_NAME_MAP.get(m, m) for m in target_metrics])}" if target_metrics else "All Metrics"
        title_text = f'{gh_str} | {metrics_str} (Clean Data)'

    fig.update_layout(
        title_text=title_text,
        height=300 * len(metrics_to_plot),
        template='plotly_white'
    )

    # --- 7. Save Chart ---
    output_filename = 'analysis/charts/greenhouse_metrics.html'
    fig.write_html(output_filename)
    print(f"Interactive plot saved to {output_filename}")

# --- Main execution block ---
if __name__ == "__main__":
    # To run from the command line with specific parameters, this block is executed.
    # In IPython, you would import and call generate_plot() directly with arguments.
    default_greenhouses = ['GH1', 'GH3', 'Nursery']
    default_metrics = ['sys_gh_temp', 'sys_h20_temp', 'fwater_temp']
    generate_plot(target_greenhouses=default_greenhouses, target_metrics=default_metrics)
