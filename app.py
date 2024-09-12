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

###

# url = "https://www.parkrun.org.uk/parkrunner/1674/5k"

# headers={
#   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#   'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
#   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
# }

# page = requests.get(url,headers=headers, verify=False) #verify= False to stop issue with limit
# soup = BeautifulSoup(page.text, 'html.parser')

# # The third table is the table of 5k results
# results_table = soup.find_all('table')[2]
# #results_table_df = pd.read_html(str(results_table))

# html_string_io = StringIO(str(results_table))
# results_table_df = pd.read_html(html_string_io)[0]

# # Step 1: Convert the date and time strings
# results_table_df['Run Date'] = pd.to_datetime(results_table_df['Run Date'], format='%d/%m/%Y')
# results_table_df['Time'] = pd.to_timedelta('00:' + results_table_df['Time']).dt.total_seconds()

# #print(results_table_df)
# results_table_df.info()

#results_table_df = scraper.get_results_table(1674)
#fig = graphs.plot_results(results_table_df)



############################################


# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)

# App layout
app.layout = [
    html.Div(className='row', children='My First App with Data, Graph, and Controls',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                       value='lifeExp',
                       inline=True,
                       id='my-radio-buttons-final'),
        dcc.Input(id="parkrun_id", type="number", placeholder="", debounce=True),
        html.Button(id='submit-button-parkrunid', n_clicks=0, children='Submit')               
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='histo-chart-final')
        ])

    ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(figure= {}, id='park_run_result_plot')
        ])
    ])
]

# Add controls to build the interaction
@callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)

def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

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
