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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##################################
###          TOTAL             ###
##################################

total_eas = 100
total_pledged = 10
total_donated = 1

total_div = html.Div([
    html.H4(f'{total_eas} Effective Altruists'),
    html.H5(f'Have donated ${total_donated}'),
    html.H5(f'And pledged another ${total_pledged}'),
])

##################################
###       DEMOGRAPHICS         ###
##################################

demo_pies = []
for table_name in [
        'age_group', 'diet', 'gender', 'employment', 'ethnicity', 'subject',
        ]:

    path = f"./rp_survey_data/{table_name}.csv"
    demo_table = pd.read_csv(path, sep='\t')
    title = demo_table.columns[0]

    # remove the 'Total' row
    demo_table = demo_table[ ~demo_table[title].isin(['Total', 'Total respondents']) ]
    demo_table['label'] = demo_table[title] + demo_table['Percent']
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))


    pie_fig = px.pie(demo_table, values='Percent', names=title, title=title)#, hovertext='label')
    # pie_fig.update_trace(hovertemplate=)
    pie_fig.update_traces(hoverinfo='none', textinfo='label')
    # pie_fig.update_traces(textposition='inside')
    pie_fig.update_traces(insidetextorientation='horizontal')
    pie_fig.update(layout_showlegend=False)
    pie_fig.update_layout(
        margin=dict(l=50, r=50, t=0, b=0),
    )
    this_pie = dcc.Graph(
        id=title, #style={'margin': '0%'},
        figure=pie_fig,
        # style={},
    )

    demo_pies.append(this_pie)

demo_pies = []
labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
          "Rest of World"]

# Create subplots: use 'domain' type for Pie subplot
demo_fig = make_subplots(
  rows=1, cols=2, 
  specs=[[{'type':'domain'}, {'type':'domain'}]], 
  subplot_titles=['1980', '2007']
)
demo_fig.add_trace(
  go.Pie(
    labels=labels, 
    values=[16, 15, 12, 6, 5, 4, 42], 
    name="GHG Emissions",
  ),
  1, 1
)
demo_fig.add_trace(
  go.Pie(labels=labels, values=[27, 11, 25, 8, 1, 3, 25], name="CO2 Emissions"),
  1, 2
)



# Use `hole` to create a donut-like pie chart
demo_fig.update_traces(hoverinfo="label+percent")

demo_fig.update_layout(
    title_text="Global Emissions 1990-2011",
    # Add annotations in the center of the donut pies.
    # annotations=[dict(text='GHG', x=0.18, y=0.5, font_size=20, showarrow=False),
                 # dict(text='CO2', x=0.82, y=0.5, font_size=20, showarrow=False)]
)

demo_pies.append(dcc.Graph(figure=demo_fig))





for table_name in [
        'age_group', 'diet', 'gender', 'employment', 'ethnicity', 'subject',
        ]:

    path = f"./rp_survey_data/{table_name}.csv"
    demo_table = pd.read_csv(path, sep='\t')
    title = demo_table.columns[0]

    # remove the 'Total' row
    demo_table = demo_table[ ~demo_table[title].isin(['Total', 'Total respondents']) ]
    demo_table['label'] = demo_table[title] + demo_table['Percent']
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))


##################################
###         WORLD MAP          ###
##################################

# source: https://plotly.com/python/bubble-maps/

countries = pd.read_csv('./rp_survey_data/country2.csv')
countries['Responses'] = countries['Responses'].astype('int')

# https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo.html
map_fig = px.scatter_geo(countries, 
                     locations="Country", #color="continent",
                     hover_name="Country", 
                     # hover_data=['Country', 'Responses'],
                     locationmode='country names',
                     size="Responses",
                     projection="equirectangular" # 'orthographic' is fun
)
map_fig.update_layout(
    margin=dict(l=00, r=00, t=0, b=0),
)

##################################
###         FUNDING            ###
##################################

funding = pd.DataFrame(columns=['Source', 'Cause Area', 'Organization', 'Amount'])

# Parse open philanthropy grants
op_grants = pd.read_csv('./openphil_grants.csv')
op_grants = op_grants[['Organization Name', 'Focus Area', 'Amount']]
op_grants.rename(columns={
    'Organization Name': 'Organization', 
    'Focus Area': 'Cause Area', 
    'Amount': 'Amount'
}, inplace=True)
op_grants['Source'] = 'Open Philanthropy'
funding = funding.append(op_grants)

# Get a list of all funding-related entities
entities = set()
for col in ['Source', 'Cause Area', 'Organization']:
    entities.update(funding[col])
entities = list(entities)

# Convert financial inputs and outputs into indices
entity2idx = {x: i for i,x in enumerate(entities)}
sources = list(funding['Source'].map(entity2idx))
targets = list(funding['Cause Area'].map(entity2idx))

# Parse funding amounts
funding['Amount'] = funding['Amount'].apply(lambda x: int(x[1:].replace(',', '') if type(x)==str else 0)).astype('int')

# Create Sankey diagram
funding_fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = entities,
      color = "blue"
    ),
    link = dict(
      source = sources, # indices correspond to labels, eg A1, A2, A2, B1, ...
      target = targets,
      value = funding['Amount']
  ))])


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
          total_div,  

          # Demographics
          html.Div(
            demo_pies, 
            style={
              'columnCount': 1, 
              # 'padding': '0px 0px 0px 200px',
            }
          ),

        ], 
        style={
          'width': '25%',
          'background-color': 'red',
          'padding': '10px',
          # 'height': '500px',
          'float': 'left', 
          # 'display': 'inline-block'
        }
      ),

      # MIDDLE #

      html.Div(
        [

          # Map
          dcc.Graph(
              id='map_fig',
              figure=map_fig
          )

        ], 
        style={
          'width': '40%', 
          'background-color': 'blue',
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
          'width': '30%', 
          'background-color': 'orange',
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