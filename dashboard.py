"""
@breif Software for displaying all collected data from EOSS flight in one dashboard

@author Demeaus Wong <------ (Please add your name here if you work on this file!)
@python version 3.8.2
@date 7/20/21
@bugs None yet!

@TODO create basic dashboard, read in csv data files, display sensor data in charts, create 3D representation of flight data, display video
    * Slider controls time represented by graphs
    * Trace data in real-time
    # Add labels for key points

"""

# -*- coding: utf-8 -*-

# Run this app with `python dashboard.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import pandas as pd

# Read data
df = pd.read_csv("Test_Data/dummy.csv")

# Link stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
h_sm = 400
w_sm = 600
h_md = 650
w_md = 800


# Start dashboard
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# fig = px.bar(df1, x="Fruit", y="Amount", color="City", barmode="group")

# Populate dashboard
app.layout = html.Div(children=[
    html.H1(children='Mission Control'),

    html.Div(children='''
        Dashboard for Edge of Space Colorado Springs 2021
    '''),

    dcc.Graph(
    figure=dict(
        data=[
            dict(
                # TODO: use timestamps as labels for x-axis
                x=[*range(0,10)],
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
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=50, b=30)
        )
    ),
    style={'height': h_sm, 'width': w_sm},
    id='gas-1'
    ),

    dcc.Graph(
    figure=dict(
        data=[
            dict(
                # TODO: use timestamps as labels for x-axis
                x=[*range(0,10)],
                y=df['TVOC'],
                name='Total Volatile Organic Compounds (ppb)',
                marker=dict(
                    color='rgb(55, 83, 109)'
                )
            )

            # dict(
            #     # TODO: use timestamps as labels for x-axis
            #     x=[*range(0,10)],
            #     y=df['H20'],
            #     name='H20?',
            #     marker=dict(
            #         color='rgb(55, 83, 109)'
            #     )
            # ),
            # dict(
            #     # TODO: use timestamps as labels for x-axis
            #     x=[*range(0,10)],
            #     y=df['Ethanol'],
            #     name='Ethanol',
            #     marker=dict(
            #         color='rgb(55, 83, 109)'
            #     )
            # ),
        ],
        layout=dict(
            title='Total Volatile Organic Compounds (ppb)',
            showlegend=False,
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=30)
        )
    ),
    style={'height': h_sm, 'width': w_sm},
    id='gas-2'
    ),

    dcc.Slider(
    min=-5,
    max=10,
    step=0.5,
    value=-3
    ),

    # html.Div(id='slider-output-container')
])

# @app.callback(
#     dash.dependencies.Output('slider-output-container', 'children'),
#     [dash.dependencies.Input('my-slider', 'value')])

def update_output(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)