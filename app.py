# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import requests
from io import StringIO
import graphs
import scraper
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


app = Dash(external_stylesheets=[dbc.themes.CYBORG])
load_figure_template('CYBORG')

# App layout
app.layout = [
    html.Div(children='View Parkrun Summary Statistics',
             style={'textAlign': 'center', 'fontSize': 30}),

    html.Div(children=[
        dbc.Input(id="parkrun_id", type="number", placeholder="", debounce=True),
        dbc.Button("Submit",id='submit-button-parkrunid',color="primary", n_clicks=0)               
    ]),

    html.Div(children=[
        html.Div(className='six columns', children=[
            dcc.Graph(figure= {}, id='park_run_result_plot')
        ])
    ])
]

# Add controls to build the interaction

@callback(
    Output(component_id='park_run_result_plot', component_property='figure'),
    Input('submit-button-parkrunid', 'n_clicks'),
    State(component_id='parkrun_id', component_property='value')
)

def update_result_graph(n_clicks,id):
    if n_clicks != 0:
        results_table_df = scraper.get_results_table(id)
        fig = graphs.plot_results(results_table_df)
        return fig
    else:
        return go.Figure()



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
