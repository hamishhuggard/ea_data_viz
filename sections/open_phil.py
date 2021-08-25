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
op_grants['Organization Name'] = op_grants['Organization Name'].apply(lambda x: 'Alliance for Safety and Justice Action Fund' if x=='Alliance for Safety and Justice' else x)

op_orgs = op_grants.groupby(by='Organization Name', as_index=False).sum().sort_values(by='Amount')
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


class OpenPhil(html.Div):
    def __init__(self):
        super(OpenPhil, self).__init__(
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
                    [
                        html.Div(
                            [
                                html.Div(
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            cause_bar_graph,
                                            style = {
                                                'height': '50%',
                                                'overflow-y': 'scroll',
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
                                ),
                            ],
                            className = 'grid-cols-3-1',
                        ),
                        html.Div(
                            # datatable
                        ),
                    ],
                    className = 'grid-rows-2-1',
                    style = {
                        'height': '85vh',
                    }
                ),
            ], # + growing_figs,
            className = 'section'
        )
