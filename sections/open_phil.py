import plotly.express as px
import pandas as pd
import numpy as np
import string
import dash_core_components as dcc
import dash_html_components as html
from utils.ea_bar_graph import EABarGraph
import math

op_grants = pd.read_csv('./data/openphil_grants.csv')
op_grants['Amount'] = op_grants['Amount'].apply(lambda x: int(x[1:].replace(',','')) if type(x)==str else x)
op_grants = op_grants.dropna()
op_grants['Focus Area'] = op_grants['Focus Area'].apply(lambda x: x.replace('Artificial Intelligence', 'AI'))
op_grants = op_grants[::-1]
# op_grants = op_grants.sort_values(by='Date', ascending=False)
print(op_grants)

op_grants['Grant'] = op_grants['Grant']# .apply(lambda x: x.split('(')[0])

op_grants['Organization Name'] = op_grants['Organization Name'].apply(lambda x: x.strip() if type(x)==str else x)
op_grants['Organization Name'] = op_grants['Organization Name'].apply(lambda x: 'Helen Keller International' if x=='Hellen Keller International' else x)

def force_length(string, length):
    if len(string) < length:
        pad = (length - len(string))
        lpad = math.floor( pad / 2 )
        rpad = math.ceil( pad / 2 )
        return '_'*lpad + string + '_'*rpad
        return string.rjust(length)
    else:
        return string[:length-3] + '...'

def display_row(row):
    grant = force_length(
        row['Grant'].split('(')[0].split('—')[-1],
        25
    )
    org = force_length( row['Organization Name'], 45 )
    amount = str(int(row['Amount']))
    amount = '_'*(8 - len(amount)) + '$' + amount
    date = row['Date']
    string = f"{grant}_{org}_{amount}__{date}".lstrip('_')
    print(string)
    return string

op_grants['x'] = op_grants.apply(display_row, axis=1)
op_grants['y'] = op_grants['Amount']
height_per_bar = 25 if len(op_grants) > 10 else 28
height = height_per_bar * len(op_grants) + 30
grant_bar_graph = EABarGraph(op_grants, height=height, title='Grants')

op_orgs = op_grants.groupby(by='Organization Name', as_index=False).sum().sort_values(by='Amount')
print(op_orgs.loc[::-1].iloc[:10])
op_orgs['x'] = op_orgs['Organization Name'].apply(lambda x: x if len(x) < 30 else x[:27]+'...')
op_orgs['y'] = op_orgs['Amount']
height_per_bar = 25 if len(op_orgs) > 10 else 28
height = height_per_bar * len(op_orgs) + 30
org_bar_graph = EABarGraph(op_orgs, height=height, title='Donee Organization')

op_causes = op_grants.groupby(by='Focus Area', as_index=False).sum().sort_values(by='Amount')
# collapse the bottom 3 cause areas
op_causes['x'] = op_causes['Focus Area']
op_causes['y'] = op_causes['Amount']
height_per_bar = 23 # 25 if len(op_causes) > 10 else 28
height = height_per_bar * len(op_causes) + 20
cause_bar_graph = EABarGraph(op_causes, height=height, title='Focus Area')


content = html.Div(
    [
        html.Div(
            html.H2('Open Philanthropy Grants'),
            className='section-heading',
        ),
        html.P([
            'Data source: ',
            dcc.Link(
                'Open Philanthropy Grants Database',
                href='https://www.openphilanthropy.org/giving/grants'
            ),
        ]),
        html.Div(
            grant_bar_graph,
            style = {
                'width': '70%',
                'height': '85vh',
                'overflow-y': 'scroll',
                'float': 'left',
            }
        ),
        html.Div(
            [
                html.Div(
                    cause_bar_graph,
                    style = {
                        'height': '50%',
                        # 'overflow-y': 'scroll',
                    }
                ),
                html.Div(
                    org_bar_graph,
                    style = {
                        'height': '50%',
                        'overflow-y': 'scroll',
                    }
                )
            ],
            style = {
                'width': '30%',
                'height': '85vh',
                # 'overflow-y': 'scroll',
                'float': 'left',
            }
        )
    ], # + growing_figs,
    className = 'section'
)
