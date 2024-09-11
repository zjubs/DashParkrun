import plotly.express as px
import plotly.graph_objects as go

def format_seconds_to_mmss(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f'{minutes:02d}:{sec:02d}'

def plot_results(results_table_df):


    # Step 2: Create the bar chart
    fig = px.bar(results_table_df, x='Run Date', y='Time', title="Time Spent by Date")

    # Step 3: Manually format y-axis ticks to mm:ss


    # Generate tick values and labels
    tickvals = list(range(0, int(results_table_df['Time'].max()) + 60, 300))  # Every minute
    ticktext = [format_seconds_to_mmss(t) for t in tickvals]

    fig.update_layout(
        yaxis=dict(
            title='Time (mm:ss)',
            tickvals=tickvals,  # Set tick values
            ticktext=ticktext,  # Set custom tick labels
        )
    )

    # Step 4: Customize hover information
    fig.update_traces(
        hovertemplate='%{x}<br>Time: %{customdata}<extra></extra>',
        customdata=[format_seconds_to_mmss(t) for t in results_table_df['Time']]
    )

    # Step 5: Add star markers where 'PB?' == 'PB'
    pb_mask = results_table_df['PB?'] == 'PB'

    fig.add_trace(
        go.Scatter(
            x=results_table_df.loc[pb_mask, 'Run Date'],
            y=results_table_df.loc[pb_mask, 'Time'],
            mode='markers',
            marker=dict(
                symbol='star',
                size=15,
                color='gold',
                line=dict(color='gold', width=2)
            ),
            name='PB',
            hoverinfo='skip'  # Skip hover for the stars (optional)
        )
    )

    return fig
