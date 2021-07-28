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

# -*- coding: utf-8 -*-

# Run this app with `python dashboard.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from ast import Div
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pandas.core.indexes import base

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.dates as mdates

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

# Stylesheets in assets folder are automatically linked

margin=dict(l=50, r=0, t=50, b=30)

# x-axis of timestamps of datetime type
df['TimeStamp'] = df['TimeStamp'].apply(lambda row : parse_timestamp(row))
x_time = df['TimeStamp']

x_time_labels = (x_time.astype({'TimeStamp': str})).to_dict()

#######################################

# Making a 'continuous' list of values between the start and stop time
# startTime = pd.Timestamp(2021, 7, 24, 8, 8, 10) # Made-up start time at 08:08:10
# endTime = pd.Timestamp(2021, 7, 24, 12, 34, 45) # Made-up end time at 12:34:45
# Specify number of points
# t = np.linspace(startTime.value, endTime.value, 100)
# Converts array to datetime objects
# t = pd.to_datetime(t)

# Discrete x needs to be a certain type for curve-fitting
x_num = mdates.date2num(x_time)
# Discrete y
y = df['Temperature']

# Fit a line to discrete x and y
z = np.polyfit(x_num, y, 3)
f = np.poly1d(z)

# 'Continuous' x
xx = np.linspace(x_num.min(), x_num.max(), 100)
xx_date = mdates.num2date(xx)

# # 'Continuous' y
yy = f(xx)

# # Example data (a circle).
# resolution = 20
# t = np.linspace(0, np.pi * 2, resolution)
# y = np.sin(t)

# # Example app.
# figure = dict(data=[{'x': [], 'y': []}], layout=dict(xaxis=dict(range=[-1, 1]), yaxis=dict(range=[-1, 1])))
# app = dash.Dash(__name__, update_title=None)  # remove "Updating..." from title
# app.layout = html.Div([dcc.Graph(id='graph', figure=figure), dcc.Interval(id="interval")])

##########################



# Start dashboard
app = dash.Dash(__name__)

# Initialize graphs as simply data in dicitonary form, not as dash core components
base_graphs = [
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
                showlegend=False,
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
                title='Total Volatile Organic Compounds (ppb)',
                showlegend=False,
                margin=margin
            )
        ),

    # Graph 3: Temperature
    # dict(
    #         data=[
    #             dict(
    #                 x=x_time,
    #                 y=df['Temperature'],
    #                 name='Temperature (ºF)',
    #                 marker=dict(
    #                     color='rgb(55, 83, 109)'
    #                 )
    #             )
    #         ],
    #         layout=dict(
    #             title='Temperature (ºF)',
    #             showlegend=False,
    #             margin=margin
    #         )
    #     )
]

test_fig = dict(
            data=[
                dict(
                    x=xx_date,
                    y=yy,
                    name='Fitted',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ), 
                dict(
                    x=x_time,
                    y=y,
                    name='Actual',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    )
                )
            ],
            layout=dict(
                title='Test',
                margin=margin
            )
        )

# List to hold objects ready to be added to the dashboard
base_objects = []

# Wrap graph data in dash core component wrapper and add to list of objects (base_objects)
i = 0
for fig in base_graphs:
    base_objects.append(
        html.Div(id='div-graph-' + str(i), className="one-third column module", children=[
            dcc.Graph(
                figure=fig,
                id='graph-' + str(i))
            ]
        )
    )
    i = i + 1

# Time Control Slider
slider = dcc.Slider(
        id='time-slider',
        min=0,
        max=len(x_time_labels),
        #TODO: Mark key events like launch time, balloon burst time, point of contact
        #TODO: Format markings, perhaps truncate timestamp to only include time or make the slider vertical
        marks=x_time_labels, 
        step=None,
    )

# Populate dashboard
# TODO: Make dashboard responsive. See style.css and container class
app.layout = html.Div(id='layout', className='', children=[
    html.H1(id='title', children='Mission Control'),
    html.Div(id='subtitle', children='''Dashboard for Edge of Space Colorado Springs 2021'''),

    
    html.Div(id='row-1', className='row', children=[
        # GoPro Side View
        html.Div(className='one-third column module', children=[html.Iframe(src="https://www.youtube.com/embed/kFr3kiLse5U", className='video')]),
        # TODO: Insert 3D Map
        html.Div(className='one-third column module', children=[]),
        # GoPro Bottom View
        html.Div(className='one-third column module', children=[html.Iframe(src="https://www.youtube.com/embed/ieX1vjXe5JE", className='video')])]
    ),

    # Graphs
    html.Div(id='row-2', className='row', children=[
        html.Div(id='graphs-output')]
    ),

    html.Div(children=[
        dcc.Graph(figure=test_fig)
    ]),

    # Time Slider
    html.Div(children=[slider])
])
# @app.callback(
#     Output(),
#     [Input()]
# )


# @app.callback(
#     Output('graphs-output', 'children'),
#     [Input('time-slider', 'value')]
# )
# Dash calls this function internally to update the the callback graphs-output children when the time-slider value changes
# idx is the value of the time slider
def update_figure(idx):
    if idx is None:
        return html.Div(base_objects)
    else:
        mod_graphs = []
        filter_x = x_time.head(idx)
        for fig in base_graphs:
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
            mod_graphs.append(mod_figure)

        mod_objects = []
        i = 0
        # Wrap figures
        for fig in mod_graphs:
            mod_objects.append(
                html.Div(id='div-graph-' + str(i), className="one-third column module", children=[
                    dcc.Graph(
                        figure=fig,
                        id='graph-' + str(i)
                    )]
                )
            )
            i = i + 1
        return html.Div(mod_objects)

if __name__ == '__main__':
    app.run_server(debug=True)