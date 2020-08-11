import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import re
from glob import glob

##################################
###         FUNDING            ###
##################################

funding = pd.DataFrame(columns=['Source', 'Cause Area', 'Organization', 'Amount'])

# Parse open philanthropy grants
op_grants = pd.read_csv('./data/openphil_grants.csv')
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
