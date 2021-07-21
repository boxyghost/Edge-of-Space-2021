"""
@breif Software for displaying all collected data from EOSS flight in one dashboard

@author Demeaus Wong <------ (Please add your name here if you work on this file!)
@python version 3.8.2
@date 7/20/21
@bugs None yet!

@TODO create basic dashboard, read in csv data files, display sensor data in charts, create 3D representation of flight data, display video
    * Slider controls vertical line along graphs
        * Show all data, If marker is after the slider value, reduce opacity and highlight with a line
    * Incorporate GPS
    * Incorporate video
    * Trace data in real-time
    * Add labels for key points
    * Make the graphs the same size so they align vertically
    * FIXME:Expand titles

"""
# Run this app with `python dashboard.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pandas.core.indexes import base

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime

############# Helpers #############

# Input: timestamp string
# Output: datetime object; timestamp pieces in a list: [year, month, day, hour, minute, second]
def parse_timestamp(timestamp):
    # Break date into parts
    timestamp_list = timestamp.split('-')
    # Break time into parts
    second = timestamp_list[-1].split('_')
    # Remove unplit time from list
    timestamp_list.pop()
    # Combine date and time lists into one
    for e in second:
        timestamp_list.append(e)
    return datetime.datetime(int(timestamp_list[0]), int(timestamp_list[1]), int(timestamp_list[2]), int(timestamp_list[3]), int(timestamp_list[4]), int(timestamp_list[5]))

############## Main ##############

# Read data
# df = pd.read_csv("Test_Data/newCoolTemp.csv")
df = pd.read_csv("Test_Data/dummy.csv")

# Link stylesheet
external_stylesheets = ['style.css']
h_sm = 400
w_sm = 600
h_md = 650
w_md = 800

margin=dict(l=50, r=0, t=50, b=30)

# x-axis of timestamps of datetime type
df['TimeStamp'] = df['TimeStamp'].apply(lambda row : parse_timestamp(row))
x_time = df['TimeStamp']

x_time_labels = (x_time.astype({'TimeStamp': str})).to_dict()

# Start dashboard
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__)

# Initialize figures
base_figures = [
    # Graph 1: Equivalent Calculated Carbon-Dioxide
        dict(
            data=[
                dict(
                    x=x_time,
                    y=df['eCO2'],
                    name='Equivalent Calculated Carbon-Dioxide (ppm)',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
            ],
            layout=dict(
                title='Equivalent Calculated Carbon-Dioxide (ppm)',
                margin=margin
            )
        ),

    # Graph 2: Total Volatile Organic Compounds
    dict(
            data=[
                dict(
                    x=x_time,
                    y=df['TVOC'],
                    name='Total Volatile Organic Compounds (ppb)',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                )
            ],
            layout=dict(
                title='Total Volatile Organic Compounds (ppb)'
            )
        ),

    # Graph 3: Temperature
    dict(
            data=[
                dict(
                    x=x_time,
                    y=df['Temperature'],
                    name='Temperature (ºF)',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                )
            ],
            layout=dict(
                title='Temperature (ºF)',
                showlegend=False,
                margin=margin
            )
        )
]

# Wrap figures
base_graphs = []
i = 0
for fig in base_figures:
    base_graphs.append(
            dcc.Graph(
                figure=fig,
                style={'height': h_sm, 'width': w_sm},
                id='graph-' + str(i)
            )
        )
    i = i + 1

# Time Control Slider
slider = dcc.Slider(
        id='time-slider',
        min=0,
        max=len(x_time_labels),
        marks=x_time_labels,
        step=None
    )

# Populate dashboard
app.layout = html.Div(id='layout', children=[
    html.H1(id='title', children='Mission Control'),
    html.Div(id='subtitle', children='''Dashboard for Edge of Space Colorado Springs 2021'''),
    # Graphs
    html.Div(id='my-output', className="container"),
    # Time Slider
    slider,
])

@app.callback(
    Output('my-output', 'children'),
    [Input('time-slider', 'value')]
)

def update_figure(idx):
    if idx is None:
        return html.Div(base_graphs)
    else:
        mod_figures = []
        filter_x = x_time.head(idx)
        for fig in base_figures:
            figure_name = fig['data'][0]['y'].name
            # Create new filter_y values
            filter_y = df[figure_name].head(idx)

            # Create a new figure with modified x and y
            mod_figure=dict(
                data=[
                    dict(
                        x=filter_x,
                        y=filter_y,
                        name=figure_name,
                        marker=dict(
                            color='rgb(55, 83, 109)'
                        )
                    )
                ],
                layout=dict(
                    title=figure_name,
                    showlegend=False,
                    margin=margin
                )
            )
            mod_figures.append(mod_figure)

        mod_graphs = []
        i = 0
        # Wrap figures
        for fig in mod_figures:
            mod_graphs.append(
                    dcc.Graph(
                        figure=fig,
                        style={'height': h_sm, 'width': w_sm},
                        id='graph-' + str(i),
                        className='column'
                    )
                )
            i = i + 1
        
        return html.Div(mod_graphs)

if __name__ == '__main__':
    app.run_server(debug=True)