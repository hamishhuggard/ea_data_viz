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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##################################
###          TOTAL             ###
##################################

total_eas = 100

total_div = html.Div([
    html.H4(f'{total_eas} Effective Altruists'),
    html.H5(f'Have donated ${TOTAL_PLEDGED}'),
    html.H5(f'And pledged another ${TOTAL_DONATED}'),
])

# nothing

##################################
###         WORLD MAP          ###
##################################

# source: https://plotly.com/python/bubble-maps/

countries = pd.read_csv('./data/rp_survey_data/country2.csv')
countries['Responses'] = countries['Responses'].astype('int')

# https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo.html
map_fig = px.scatter_geo(countries, 
                     locations="Country", #color="continent",
                     hover_name="Country", 
                     # hover_data=['Country', 'Responses'],
                     locationmode='country names',
                     size="Responses",
                     projection="equirectangular", # 'orthographic' is fun
                     height=150,
        # config={
        #     'displayModeBar': False,
        # },
)
map_fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
)
map_fig.update_geos(
    # resolution=50,
    showcoastlines=False, 
    # coastlinecolor="RebeccaPurple",
    # showland=True, 
    landcolor="LightBlue",
    # showocean=False,#True, oceancolor="LightBlue",
    # showlakes=True, lakecolor="Blue",
    # showrivers=True, rivercolor="Blue"
)

##################################
###          LAYOUT            ###
##################################

app.layout = html.Div(children=[

    ## HEADING ##

    html.H1(
      'Effective Altruism Dashboard',
      style={
          'float': 'center',
      }
    ),


    ## CONTENT ##

    html.Div([

      # LEFT #

      html.Div(
        [

          # Totals
          # total_div,  

          # Map
          dcc.Graph(
              id='map_fig',
              figure=map_fig
          ),

          # Demographics
          html.Div(
            demo_pies, 
            style={
              'columnCount': 2, 
              # 'padding': '0px 0px 0px 200px',
            }
          ),

        ], 
        style={
          'width': '30%',
          # 'background-color': 'red',
          'padding': '10px',
          # 'height': '400px',
          'float': 'left', 
          # 'display': 'inline-block'
        }
      ),

      # MIDDLE #

      html.Div(
        [


        ], 
        style={
          'width': '40%', 
          # 'background-color': 'blue',
          'padding': '10px',
          'float': 'left',
          # 'height': '500px',
          # 'display': 'inline-block'
        }
      ),

      # RIGHT #

      html.Div(
        [
          dcc.Graph(figure=funding_fig),
        ], 
        style={
          'width': '50%', 
          # 'background-color': 'orange',
          'padding': '10px',
          'float': 'left',
          # 'height': '500px',
          # 'display': 'inline-block'
        }
      ),

    ],
    style={
      # 'padding': '10px',
    }
    ),

    # 

])

if __name__ == '__main__':
    app.run_server(debug=True)