# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import re
from glob import glob

from funding import *
from demographics import *
from growth import *
from geography import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Effective Altruism Data Viewer'
server = app.server

##################################
###          TOTAL             ###
##################################

total_eas = 100

total_div = html.Div([
    html.H4('{total_eas} Effective Altruists'),
    html.H5('Have donated ${TOTAL_PLEDGED}'),
    html.H5('And pledged another ${TOTAL_DONATED}'),
])

# nothing



##################################
###          LAYOUT            ###
##################################

app.layout = html.Div(children=[

    ## HEADING ##

    html.Div(
      [
          html.Div(
            [
                html.Img(
                  src='https://effectivealtruism.nz/wp-content/uploads/2018/02/lightbulblogo-1.png',
                  # width=200,
                ),
                html.H1(
                  [
                    html.Span(
                      'Effective ',
                      style = {
                        'font-weight': '700',
                      }
                    ),
                    html.Span(
                      'Altruism',
                      style = {
                        'font-weight': '400',
                      }
                    )
                  ],
                  # 'Effective Altruism',
                  style = {
                    'font-family': 'Roboto Slab',
                    # 'font-weight': '700',
                  }
                ),
                html.H3(
                  'Data Visualizer',
                  style = {
                    'font-family': 'Raleway',
                  }
                )
            ],
            style = {
              'margin': '0',
              'position': 'absolute',
              'top': '35%',
              'left': '50%',
              '-ms-transform': 'translate(-50%, -50%)',
              'transform': 'translate(-50%, -50%)',
            }
          )
      ],
      className='big-box',
      style={
          'margin': '0 auto',
          'width': '100%',
          'height': '60vh',
      }
    ),

    # Demographics
    demo_div,

    # Geography
    geo_div,

    # Donations
    donation_div,

    # Growth
    growth_div,

    ],

    style={
      'width': '90%',
      'margin': '0 auto',
      'text-align': 'center',
      # 'padding': '10px',
    }
)

if __name__ == '__main__':
    app.run_server(debug=False)
