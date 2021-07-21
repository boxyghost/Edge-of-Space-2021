"""
@breif Software for displaying all collected data from EOSS flight in one dashboard

@author Demeaus Wong <------ (Please add your name here if you work on this file!)
@python version 3.8.2
@date 7/20/21
@bugs None yet!

@TODO create basic dashboard, read in csv data files, display sensor data in charts, create 3D representation of flight data, display video
    * Slider controls time represented by graphs with vertical line
    * Incorporate GPS
    * Incorporate video
    * Trace data in real-time
    * Add labels for key points

"""

# -*- coding: utf-8 -*-

# Run this app with `python dashboard.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
df = pd.read_csv("Test_Data/dummy.csv")

# Link stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
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

# Initialize graphs
# Graph 1: Equivalent Calculated Carbon-Dioxide
fig_1 = dcc.Graph(
    figure=dict(
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
    style={'height': h_sm, 'width': w_sm},
    id='graph-1'
    )

# Graph 2: Total Volatile Organic Compounds
fig_2 = dcc.Graph(
    figure=dict(
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
    style={'height': h_sm, 'width': w_sm},
    id='graph-2'
    )

# Graph 3: Temperature
fig_3 = dcc.Graph(
    figure=dict(
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
    ),
    style={'height': h_sm, 'width': w_sm},
    id='graph-3'
    )

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

    html.Div(id='subtitle', children='''
        Dashboard for Edge of Space Colorado Springs 2021
    '''),

    # Graphs
    fig_1, fig_2, fig_3,

    # Time Slider
    slider,

    html.Div(id='my-output')
])

@app.callback(
    Output('my-output', 'children'),
    [Input('time-slider', 'value')]
)

# def update_output_div(input_value):
#     return 'Output: {}'.format(input_value)

def update_figure(idx):
    dff = df
    filtered_x = x_time
    filtered_y = df['eCO2']
    if idx is None:
        return html.Div(dcc.Graph(
            figure=dict(
                data=[
                    dict(
                        x=filtered_x,
                        y=filtered_y,
                        name='2. test-graph',
                        marker=dict(
                            color='rgb(55, 83, 109)'
                        )
                    )
                ],
                layout=dict(
                    title='TESTING',
                    margin=margin
                )
            ),
            style={'height': h_sm, 'width': w_sm},
        ))
    else:
        filtered_x = x_time.head(idx)
        filtered_y = df['eCO2'].head(idx)
        return html.Div(dcc.Graph(
            figure=dict(
                data=[
                    dict(
                        x=filtered_x,
                        y=filtered_y,
                        name='2. test-graph',
                        marker=dict(
                            color='rgb(55, 83, 109)'
                        )
                    )
                ],
                layout=dict(
                    title='TESTING',
                    margin=margin
                )
            ),
            style={'height': h_sm, 'width': w_sm},
            id='test-graph'
            )
        )

if __name__ == '__main__':
    app.run_server(debug=True)