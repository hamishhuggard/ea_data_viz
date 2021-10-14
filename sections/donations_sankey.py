import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import re
from glob import glob
import os
from utils.subtitle import get_subtitle

def get_op_grants():
    op_grants = pd.read_csv('./data/openphil_grants.csv')
    # op_grants = pd.read_csv('https://www.openphilanthropy.org/giving/grants/spreadsheet')

    # Standardize cause area names
    # standard names from https://80000hours.org/topic/causes/
    subs = {
      'Potential Risks from Advanced Artificial Intelligence': 'AI',
      'History of Philanthropy': 'Other cause area',
      'Immigration Policy': 'Policy',
      'Macroeconomic Stabilization Policy': 'Policy',
      'Land Use Reform': 'Policy',
      'Criminal Justice Reform': 'Policy',
      'U.S. Policy': 'Policy',
      'Other areas': 'Other cause area',
      'Biosecurity and Pandemic Preparedness': 'Biosecurity',
      'Farm Animal Welfare': 'Animal Welfare',
      'Global Catastrophic Risks': 'Catastrophic Risks',
      'Global Health & Development': 'Global Poverty',
    }
    op_grants['Cause Area'] = op_grants['Focus Area'].map(subs).fillna(op_grants['Focus Area'])

    subs = {
    #  'Johns Hopkins Center for Health Security': 'JHCHS',
    #  'Against Malaria Foundation': 'AMF',
    #  'Georgetown University': 'GU',
    }
    op_grants['Organization'] = op_grants['Organization Name'].map(subs).fillna(op_grants['Organization Name'])

    # Standardise Column Names
    op_grants = op_grants[['Organization', 'Cause Area', 'Amount']]
    op_grants['Source'] = 'Open Philanthropy'

    def parse_funding_amount(amount):
        if type(amount)==str:
            return int(amount[1:].replace(',', ''))
        else:
            return 0
    op_grants['Amount'] = op_grants['Amount'].apply(parse_funding_amount).astype('int')

    return op_grants


def get_gwwc_and_founders_pledge():
    return pd.read_csv('data/misc.csv')


def get_ea_funds():
    ea_funds = pd.read_csv('./data/ea_funds_grants.csv')

    subs = {
        'global-development': 'Global Poverty',
        'far-future': 'Far Future',
        'ea-community': 'EA Community',
        'animal-welfare': 'Animal Welfare'
    }
    ea_funds['fund'] = ea_funds['fund'].map(subs).fillna(ea_funds['fund'])

    ea_funds['Source'] = 'EA Funds'
    ea_funds['Cause Area'] = ea_funds['fund']
    ea_funds['Organization'] = 'Unknowns'
    ea_funds['Amount'] = ea_funds['amount']
    ea_funds = ea_funds[['Source', 'Cause Area', 'Organization', 'Amount']]

    return ea_funds


def get_funding_long():

    funding = pd.concat(
        [
            get_op_grants(),
            get_gwwc_and_founders_pledge(),
            get_ea_funds(),
        ]
    )

    '''
    Transform table from
      'OpenPhil', 'Global Poverty', 'AMF', 100
      'OpenPhil', 'Global Poverty', 'SCI', 80
    to
      'OpenPhil', 'Global Poverty', 180, 'OpenPhil'
      'Global Poverty', 'AMF', 100, 'OpenPhil'
      'Global Poverty', 'SCI', 80, 'OpenPhil'
    That is, sum the contributions of each entity to each other entity.
    Each row represents a connection between two entities.
    The last column will be used for coloring the connections.
    '''

    funding['Amount'] = funding['Amount'] / 1e6

    funding_long = pd.DataFrame(columns=['From', 'To', 'Amount', 'Source'])

    for source, cause in set(
        zip(
            funding['Source'],
            funding['Cause Area']
        )
    ):

        source_cause_df = funding[
            (funding['Source']==source) & (funding['Cause Area']==cause)
        ]

        total_funding = source_cause_df['Amount'].sum()
        funding_long.loc[len(funding_long)] = [
            source,
            cause,
            total_funding,
            source
        ]

        other_total = 0
        for org in source_cause_df['Organization'].unique():
            org_df = source_cause_df[source_cause_df['Organization']==org]
            total_funding = org_df['Amount'].sum()

            if total_funding < 2*10**1:
            # if total_funding < 2*10**7:
                other_total += total_funding
                continue

            funding_long.loc[len(funding_long)] = [
                cause,
                org,
                total_funding,
                source
            ]

        if other_total > 0:
            funding_long.loc[len(funding_long)] = [
                cause,
                'Other orgs',
                other_total,
                source
            ]

    funding_long = funding_long[funding_long['To']!='Unknowns']

    return funding_long

def funding_fig():

    funding_long = get_funding_long()

    # Get a list of all funding-related entities
    entities = set()
    for col in ['From', 'To']:
        entities.update(funding_long[col])
    entities = list(entities)

    # Convert financial inputs and outputs into indices
    entity2idx = {x: i for i,x in enumerate(entities)}
    froms = list(funding_long['From'].map(entity2idx))
    tos = list(funding_long['To'].map(entity2idx))

    entities += ["$100M (for scale)"]
    froms += [ len(entity2idx) ]
    tos += [ len(entity2idx) ]

    # values = funding_long['Amount'].to_list() + [1e8]
    values = funding_long['Amount'].to_list() + [1e2]

    # Create Sankey diagram
    fig = go.Figure(
      data=[go.Sankey(
        valueformat = ",.1f",
        valuesuffix = "M USD",
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "#4196AA", width = 1),
          label = entities,
          color = "#4196AA"
        ),
        link = dict(
          source = froms, 
          target = tos,
          color = "#C1E3EA",
          value = values
        )
      )],
      # config={
      #   'displayModeBar': False,
      # }
    )
    fig.update_layout(
      margin=dict(l=10, r=10, t=30, b=10),
    )

    return fig

def donations_sankey_section():

    return html.Div(
        [
            html.Div(
                html.H2('Donations Overview'),
                className='section-title',
            ),
            get_subtitle(
                [
                    'open_phil',
                    'funds_payout',
                    'founders_pledge',
                    'gwwc',
                ],
                hover='rectangles or lines',
                extra_text = 'Rectangles can be rearranged by dragging.',
            ),
            html.Div(
                html.Div(
                    dcc.Graph(
                        id='Donations',
                        figure=funding_fig(),
                        responsive=True,
                    ),
                    className = 'plot-container',
                ),
                className = 'section-body',
            ),
        ],
        className = 'section',
        id='donations-sankey',
    )
