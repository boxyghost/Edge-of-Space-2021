"""
@breif Software for displaying all collected data from EOSS flight in one dashboard

@author Demeaus Wong <------ (Please add your name here if you work on this file!)
@python version 3.8.2
@date 7/20/21
@bugs None yet!

@TODO create basic dashboard, read in csv data files, display sensor data in charts, create 3D representation of flight data, display video
    * Dropdown allows you to select data to compare
    * Slider controls vertical line along graphs
        * Show all data, If marker is after the slider value, reduce opacity and highlight with a line https://plotly.com/python/horizontal-vertical-shapes/
    * Incorporate GPS
    * Trace data in real-time
    * Add labels for key points

"""

# -*- coding: utf-8 -*-

# Run this app with `python dashboard.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, MATCH, ALL

# import plotly.express as px
# import plotly.graph_objects as go
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

def make_dropdown_left (idx):
    drop = html.Div(
        children=[dcc.Dropdown(
            id={'type': 'left-dropdowns','index': idx},
            options=options,
            placeholder="Select a dataset"
        )],
        className='dropdown',
        style={'float':'left'}
    )
    return drop

def make_dropdown_right (idx):
    drop = html.Div(
        children=[dcc.Dropdown(
            id={'type': 'right-dropdowns','index': idx},
            options=options,
            placeholder="Select a dataset"
        )],
        className='dropdown',
        style={'float':'right'}
    )
    return drop

# Input: Data column
# Output: Fitted continuous y-values
# def curve_fitting(column):

#     return 

############## Main ##############
serial = 0 # For giving each pair of dropdowns a unique index

# Read data
df = pd.read_csv("Test_Data/dummy.csv")

headers = list(df.columns.values)
headers.pop(0) # Removes TimeStamp left_data

# Preparing values for the dropdown based on data in the csv
options = []
for header in headers:
    item = dict(
        label=header,
        value=header,
    )
    options.append(item)

# Stylesheets in assets folder are automatically linked

margin=dict(l=50, r=0, t=50, b=30)

# x-axis of timestamps of datetime type
df['TimeStamp'] = df['TimeStamp'].apply(lambda row : parse_timestamp(row))

# 
x_time = df['TimeStamp']

# Discrete x needs to be a certain type for curve-fitting
x_num = mdates.date2num(x_time)

x_time_labels = (x_time.astype({'TimeStamp': str})).to_dict()

# Initial curve-fitting
# Default Data 1: Temperature
# Discrete y
y_temperature = df[headers[0]]

# Fit a line to discrete x and y
z_temperature = np.polyfit(x_num, y_temperature, 3)
f_temperature = np.poly1d(z_temperature)

# 'Continuous' x
xx = np.linspace(x_num.min(), x_num.max(), 100)
xx_date = mdates.num2date(xx)

# 'Continuous' y
yy_temperature = f_temperature(xx)

# Default Data 2: Humidity
# Discrete y
y_humidity = df[headers[1]]

# Fit a line to discrete x and y
z_humidity = np.polyfit(x_num, y_humidity, 3)
f_humidity = np.poly1d(z_humidity)

# 'Continuous' y
yy_humidity = f_humidity(xx)

#######################################

# Example of autoplay
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

# Initialize graphs as simply data in dictionary form, not as dash core components
base_graphs = [
    # Graph 1
        dict(
            data=[
                dict(
                    x=xx_date,
                    y=yy_temperature,
                    name='Fitted Temperature',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    )
                ), 
                dict(
                    x=x_time,
                    y=y_temperature,
                    name='Actual Temperature',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    ),
                    mode='markers'
                ),
                dict(
                    x=xx_date,
                    y=yy_humidity,
                    name='Fitted Humidity',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    )
                ), 
                dict(
                    x=x_time,
                    y=y_humidity,
                    name='Actual Humidity',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    ),
                    mode='markers'
                )

            ],
            layout=dict(
                title='Test 1',
                margin=margin,
                legend=dict(
                    orientation="h"
                ),
                xaxis=dict(
                    range=[x_time.min() - datetime.timedelta(minutes=10), x_time.max() + datetime.timedelta(minutes=10)]
                )
            )
        ),

    # Graph 2
    dict(
            data=[
                dict(
                    x=xx_date,
                    y=yy_temperature,
                    name='Fitted Temperature',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    )
                ), 
                dict(
                    x=x_time,
                    y=y_temperature,
                    name='Actual Temperature',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    ),
                    mode='markers'
                ),
                dict(
                    x=xx_date,
                    y=yy_humidity,
                    name='Fitted Humidity',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    )
                ), 
                dict(
                    x=x_time,
                    y=y_humidity,
                    name='Actual Humidity',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    ),
                    mode='markers'
                )

            ],
            layout=dict(
                title='Test 2',
                margin=margin,
                legend=dict(
                    orientation="h"
                ),
                xaxis=dict(
                    range=[x_time.min() - datetime.timedelta(minutes=10), x_time.max() + datetime.timedelta(minutes=10)]
                )
            )
        ),

    # Graph 3
    dict(
            data=[
                dict(
                    x=xx_date,
                    y=yy_temperature,
                    name='Fitted Temperature',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    )
                ), 
                dict(
                    x=x_time,
                    y=y_temperature,
                    name='Actual Temperature',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    ),
                    mode='markers'
                ),
                dict(
                    x=xx_date,
                    y=yy_humidity,
                    name='Fitted Humidity',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    )
                ), 
                dict(
                    x=x_time,
                    y=y_humidity,
                    name='Actual Humidity',
                    marker=dict(
                        color='rgb(25, 103, 109)'
                    ),
                    mode='markers'
                )

            ],
            layout=dict(
                title='Test 3',
                margin=margin,
                legend=dict(
                    orientation="h"
                ),
                xaxis=dict(
                    range=[x_time.min() - datetime.timedelta(minutes=10), x_time.max() + datetime.timedelta(minutes=10)]
                )
            )
        )
]

# List to hold objects ready to be added to the dashboard
base_objects = []

# Wrap graph data in dash core component wrapper and add to list of objects (base_objects)
i = 0
for fig in base_graphs:
    base_objects.append(
        html.Div(
            className="one-third column module", children=[
            html.Div(className='dropdowns', children=[
                make_dropdown_left(serial),
                make_dropdown_right(serial)
            ]),
            dcc.Graph(
                figure=fig,
                id={'type': 'dynamic-graphs', 'index': i} 
                )
            ]
        )
    )
    serial += 1
    i += 1

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
app.layout = html.Div(id='layout', style={"background-image": "url('assets/EOS.jpg')"}, className='', children=[
    
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

    # html.Div(id='test-output', children=[]),

    # Graphs
    html.Div(id='row-2', className='row', children=[
        html.Div(id='graphs-output')]
    ),

    # Time Slider
    html.Div(children=[slider])
])

# For updating graphs with left dropdowns
# TODO: Only affect one part of the graphs data; the 'left side'
@app.callback(
    Output({'type': 'dynamic-graphs', 'index': MATCH}, 'figure'),
    [Input({'type': 'left-dropdowns', 'index': MATCH}, 'value')],
    [Input({'type': 'right-dropdowns', 'index': MATCH}, 'value')],
    # prevent_initial_callback=True
)
def update_left_y(left_data, right_data):
    if left_data == None:
        left_data =headers[0]
    if right_data == None:
        right_data =headers[0]

    # Curve-fitting for the selected left_data and right_data from dropdowns
    # Discrete y
    y_left = df[left_data]

    # Fit a line to discrete x and y
    z_left = np.polyfit(x_num, y_left, 3)
    f_left = np.poly1d(z_left)

    # 'Continuous' y
    yy_left = f_left(xx)

    # Default Data 2: Humidity
    # Discrete y
    y_right = df[right_data]

    # Fit a line to discrete x and y
    z_right = np.polyfit(x_num, y_right, 3)
    f_right = np.poly1d(z_right)

    # 'Continuous' y
    yy_right = f_right(xx)

    mod_figure=dict(
                data=[
                    dict(
                        x=xx_date,
                        y=yy_left,
                        name='Fitted ' + left_data,
                        marker=dict(
                            color='rgb(25, 103, 109)'
                        )
                    ), 
                    dict(
                        x=x_time,
                        y=y_left,
                        name='Actual '+ left_data,
                        marker=dict(
                            color='rgb(25, 103, 109)'
                        ),
                        mode='markers'
                    ),
                    dict(
                        x=xx_date,
                        y=yy_right,
                        name='Fitted ' + right_data,
                        marker=dict(
                            color='rgb(25, 103, 109)'
                        )
                    ), 
                    dict(
                        x=x_time,
                        y=y_right,
                        name='Actual ' + right_data,
                        marker=dict(
                            color='rgb(25, 103, 109)'
                        ),
                        mode='markers'
                    )
                ],
                layout=dict(
                    title= left_data + ' vs. ' + right_data,
                    margin=margin,
                    legend=dict(
                        orientation="h"
                    ),
                    xaxis=dict(
                        range=[x_time.min() - datetime.timedelta(minutes=10), x_time.max() + datetime.timedelta(minutes=10)]
                    )
                )
            )
    return mod_figure

@app.callback(
    Output('graphs-output', 'children'),
    [Input('time-slider', 'value')]
)
# Dash calls this function internally to update the the callback graphs-output children when the time-slider value changes
# idx is the value of the time slider
def update_graphs(idx):
    if idx is None:
        return html.Div(base_objects)
    else:
        mod_graphs = []
        # filter_x = x_time.head(idx)
        # TODO: Change this from a for-loop to be dependent dropdowns
        # TODO: Display two y-axis for each selected dataset
        for fig in base_graphs:
            # figure_name = fig['data'][0]['y'].name
            # Create new filter_y values
            # filter_y = df[figure_name].head(idx)

            # Create a new figure with modified x and y
            mod_figure=dict(
                data=[
                    dict(
                        x=xx_date,
                        y=yy_temperature,
                        name='Fitted Temperature',
                        marker=dict(
                            color='rgb(25, 103, 109)'
                        )
                    ), 
                    dict(
                        x=x_time,
                        y=y_temperature,
                        name='Actual Temperature',
                        marker=dict(
                            color='rgb(25, 103, 109)'
                        ),
                        mode='markers'
                    ),
                    dict(
                        x=xx_date,
                        y=yy_humidity,
                        name='Fitted Humidity',
                        marker=dict(
                            color='rgb(25, 103, 109)'
                        )
                    ), 
                    dict(
                        x=x_time,
                        y=y_humidity,
                        name='Actual Humidity',
                        marker=dict(
                            color='rgb(25, 103, 109)'
                        ),
                        mode='markers'
                    )
                ],
                layout=dict(
                    title=str(idx),
                    margin=margin,
                    legend=dict(
                        orientation="h"
                    ),
                    xaxis=dict(
                        range=[x_time.min() - datetime.timedelta(minutes=10), x_time.max() + datetime.timedelta(minutes=10)]
                    )
                )
            )
            mod_graphs.append(mod_figure)

        mod_objects = []
        i = 0
        # Wrap figures
        for fig in mod_graphs:
            mod_objects.append(
                html.Div(
                    className="one-third column module", children=[
                    dcc.Graph(
                        figure=fig,
                        id={'type': 'dynamic-graphs', 'index': i},
                    )]
                )
            )
            i = i + 1
        return html.Div(mod_objects)

if __name__ == '__main__':
    app.run_server(debug=True)