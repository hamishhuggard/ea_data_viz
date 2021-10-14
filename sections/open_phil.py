import plotly.express as px
import pandas as pd
import numpy as np
from dash import dcc
from dash import html
from dash import dash_table
from plots.bar import Bar
from utils.subtitle import get_subtitle
from plots.scatter import Scatter

def get_op_grants():

    op_grants = pd.read_csv('./data/openphil_grants.csv')
    op_grants['Amount'] = op_grants['Amount'].apply(
        lambda x: int(x[1:].replace(',','')) if type(x)==str else x
    )
    op_grants = op_grants.dropna()
    op_grants['Focus Area'] = op_grants['Focus Area'].apply(lambda x: x.replace('Artificial Intelligence', 'AI'))
    op_grants = op_grants[::-1]

    op_grants['Grant'] = op_grants['Grant']

    def normalize_orgname(orgname):
        if type(orgname) == str:
            orgname = orgname.strip()
        if orgname == 'Hellen Keller International':
            orgname = 'Helen Keller International'
        if orgname == 'Alliance for Safety and Justice':
            orgname = 'Alliance for Safety and Justice Action Fund'
        return orgname
    op_grants['Organization Name'] = op_grants['Organization Name'].apply(normalize_orgname)

    # for finding number of grants
    op_grants['grants'] = 1

    op_grants['Date'] = pd.to_datetime(op_grants['Date'], format='%m/%Y')
    op_grants = op_grants.sort_values(by='Date', ascending=False)
    op_grants['Date_readable'] = op_grants['Date'].dt.strftime('%B %Y')

    # hovertext
    def hover(row):
        grant = row['Grant']
        org = row['Organization Name']
        area = row['Focus Area']
        date = row['Date_readable']
        amount = row['Amount']
        return f'<b>{grant}</b><br>Date: {date}<br>Organization: {org}<br>Amount: ${amount:,.0f}'
    op_grants['hover'] = op_grants.apply(hover, axis=1)

    return op_grants


def org_bar_chart(op_grants):

    op_orgs = op_grants.groupby(by='Organization Name', as_index=False).sum()
    op_orgs = op_orgs.sort_values(by='Amount')
    op_orgs['x'] = op_orgs['Organization Name']
    # op_orgs['x'] = op_orgs['x'].apply(lambda x: x if len(x) < 30 else x[:27]+'...')
    op_orgs['y'] = op_orgs['Amount']
    op_orgs['text'] = op_orgs['Amount'].apply(lambda x: f'${x:,.0f}')

    # Some organization names get truncated to the same value.
    # This prevents that:
    for val in op_orgs['x'].unique():
        val_df = op_orgs[ op_orgs['x']==val ]
        for i in range(1, len(val_df)):
            index = val_df.iloc[i].name
            op_orgs.loc[index, 'x'] = op_orgs.loc[index, 'x'][:-3-i] + '...'

    def hover(row):
        org = row['Organization Name']
        amount = row['text']
        grants = row['grants']
        return f'<b>{org}</b><br>{grants} grants<br>{amount} total'
    op_orgs['hover'] = op_orgs.apply(hover, axis=1)

    op_orgs_truncated = op_orgs.iloc[len(op_orgs)-25:]

    return Bar(op_orgs_truncated, title='Top 30 Donee Organizations')


def cause_bar_chart(op_grants):

    op_causes = op_grants.groupby(by='Focus Area', as_index=False).sum()
    op_causes = op_causes.sort_values(by='Amount')
    op_causes['x'] = op_causes['Focus Area']
    op_causes['y'] = op_causes['Amount']
    op_causes['text'] = op_causes['Amount'].apply(lambda x: f'${x:,.0f}')

    def hover(row):
        area = row['Focus Area']
        amount = row['text']
        grants = row['grants']
        return f'<b>{area}</b><br>{grants} grants<br>{amount} total'
    op_causes['hover'] = op_causes.apply(hover, axis=1)

    height_per_bar = 25 if len(op_causes) > 10 else 28
    height = height_per_bar * len(op_causes) + 20
    return Bar(op_causes, height=height, title='Focus Areas')


def grants_scatter(op_grants):
    return Scatter(
        op_grants,
        x = "Date",
        y = "Amount",
        # color="Focus Area",
        # size='Amount',
        hover = 'hover',
        log_y = True,
        title = 'Individual Grants (log)',
        y_title = 'Amount (USD)',
        x_title = '',
        id = 'op-grants-scatter',
    )

# def grants_cumulative_scatter(op_grants):
#     fig = px.scatter(
#         op_grants,
#         x="Date",
#         y="Amount ($)",
#         # color="Focus Area",
#         # size='Amount',
#         hover_data=['Grant'],
#         log_y=True,
#         title='Cumulative Grants (log)',
#     )
#     fig.update_traces(
#         marker_color="#0c869b",
#         hovertext = op_grants['hover'],
#         hovertemplate = '%{hovertext}<extra></extra>',
#     )
#     fig.update_layout(
#         margin=dict(l=0, r=0, t=30, b=0),
#         xaxis=dict(
#             title='',
#         ),
#         yaxis=dict(
#             title='Amount ($)',
#         ),
#         title_x=0.5,
#         font=dict(
#             family="Raleway",
#             size=12,
#         )
#     )
#     return dcc.Graph(id='op-grants-cum-scatter', figure=fig),

# op_grants = op_grants[['Grant', 'Organization Name', 'Focus Area']]
# grants_table = dash_table.DataTable(
#     id = 'op_table',
#     columns = [{"name": i, "id": i} for i in op_grants.columns],
#     data = op_grants.to_dict('records'),
#     page_action='none',
#     fixed_rows={
#         'headers': True,
#     },
#     style_table={
#         'width': '100%',
#         'minWidth': '100%',
#         'maxWidth': '100%',
#     },
#     style_cell={
#         'whiteSpace': 'normal',
#         'height': 'auto',
#     },
#     style_cell_conditional=[
#         {'if': {'column_id': 'Grant'},
#          'width': '30%'},
#         {'if': {'column_id': 'Organization Name'},
#          'width': '20%'},
#         {'if': {'column_id': 'Focus Area'},
#          'width': '10%'},
#     ],
#     # style_cell={
#     #     # 'minWidth': 95,
#     #     'maxWidth': '30%',
#     #     'width': '100%',
#     # }
# )


def openphil_grants_scatter_section():

    op_grants = get_op_grants()

    return html.Div(
        [
            html.Div(
                html.H2('Open Philanthropy Grants'),
                className='section-title',
            ),
            get_subtitle('open_phil', hover='points', zoom=True),
            html.Div(
                [
                    html.Div(
                        grants_scatter(op_grants),
                        className='plot-container',
                    ),
                ],
                className='section-body'
            ),
        ],
        className = 'section',
        id='op-grants-scatter-section',
    )

def openphil_grants_categories_section():

    op_grants = get_op_grants()

    return html.Div(
        [
            html.Div(
                html.H2('Open Philanthropy Grants by Focus Area and Donee Organization'),
                className='section-title',
            ),
            get_subtitle('open_phil'),
            html.Div(
                html.Div(
                    [
                        html.Div(
                            cause_bar_chart(op_grants),
                            className='plot-container',
                        ),
                        html.Div(
                            org_bar_chart(op_grants),
                            className='plot-container',
                        ),
                    ],
                    className='grid desk-cols-2 tab-cols-2',
                ),
                className='section-body'
            ),
        ],
        className = 'section',
        id='op-grants-categories',
    )
