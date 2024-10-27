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
from result import Result
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


app = Dash(external_stylesheets=[dbc.themes.CYBORG])
load_figure_template('CYBORG')

card_content = [
    #dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]


# App layout
app.layout = dbc.Container([
    html.Div(children='View Parkrun Summary Statistics',
             style={'textAlign': 'center', 'fontSize': 30}),

    dbc.Row(children = [
        dbc.Col(dbc.Input(id="parkrun_id", type="number", placeholder="Enter Parkrun ID", debounce=True), width = {"size": 1, "offset": 1}),
        dbc.Col(dbc.Button("Submit",id='submit-button-parkrunid',color="primary", n_clicks=0), width = 1),
    ]),
    html.Hr(),

    dbc.Row(children=[
        dbc.Col(dcc.Graph(figure= {}, id='park_run_result_plot'), width = {"size": 6, "offset": 1}),
        dbc.Col(
            dbc.Row([
                dbc.Col(dbc.Card(card_content, color="primary", inverse=True), width=6),  # Each card takes up 6 columns (half the row)
                dbc.Col(dbc.Card(card_content, color="secondary", inverse=True), width=6),
                dbc.Col(dbc.Card(card_content, color="success", inverse=True), width=6),
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True), width=6)
            ])
                , width=2)


        # dbc.Col([
        #     dbc.Row(dbc.Card(card_content, color="primary", inverse=True)),
        #     dbc.Row(dbc.Card(card_content, color="secondary", inverse=True))]
        #     , width = 1
        # ),
        # dbc.Col([
        #     dbc.Row(dbc.Card(card_content, color="success", inverse=True)),
        #     dbc.Row(dbc.Card(card_content, color="warning", inverse=True))]
        #     , width = 1
        # ),
    ]),
    
], fluid = True)

# Add controls to build the interaction

@callback(
    Output(component_id='park_run_result_plot', component_property='figure'),
    Input('submit-button-parkrunid', 'n_clicks'),
    State(component_id='parkrun_id', component_property='value')
)

def update_result_graph(n_clicks,id):
    if n_clicks != 0:
        page = scraper.get_url(id)
        user_results = Result(page.text)
        #results_table_df = scraper.get_results_table(id)
        fig = graphs.plot_results(user_results.results_table)
        return fig
    else:
        return go.Figure()



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
