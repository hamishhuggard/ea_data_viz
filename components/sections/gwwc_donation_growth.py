import pandas as pd
from dash import html
from utils.get_data.query_gwwc import get_donations_by_year
from utils.subtitle import get_subtitle
from utils.plots.line import Line
from datetime import datetime


def get_num_donors_hover(row):

    year = row['date'].strftime('%Y')

    result = ''
    result += f"<b>{year}</b>"
    result += f"<br>${row.amount_normalized:,.2f} donations"
    result += f"<br>${row.amount_normalized_total:,.2f} total donations"
    result += f"<br>{row.num_donors:,} donors"

    return result


def get_gwwc_donation_growth_section():

    donations_by_year = pd.read_json('./data/gwwc/donations_by_year.json')
    #donations_by_year = get_donations_by_year()

    donations_by_year['date'] = pd.to_datetime(donations_by_year['year'], format='%Y')
    donations_by_year = donations_by_year.sort_values(by='date')

    # Filter out future donations
    donations_by_year = donations_by_year.loc[ donations_by_year['date'] < datetime.now() ]

    donations_by_year['amount_normalized_total'] = donations_by_year['amount_normalized'].cumsum()

    donations_by_year['hover'] = donations_by_year.apply(get_num_donors_hover, axis=1)

    donations_by_year['label'] = 'Donations'

    label = donations_by_year['amount_normalized'].tolist()[-1]
    last_year = int(donations_by_year['year'].tolist()[-1])
    label = f'<b>{last_year} Donations</b><br>${label/1e6:,.1f} Million'
    donations_by_year['label'] = label

    annual_donations_graph = Line(
        donations_by_year,
        x='date',
        y='amount_normalized',
        title='Annual Donation Amounts',
        x_title='',
        y_title='',
        hover='hover',
        dollars=True,
    )

    label = donations_by_year['amount_normalized_total'].tolist()[-1]
    label = f'<b>Total Donated</b><br>${label/1e6:,.1f} Million'
    donations_by_year['label'] = label

    total_donations_graph = Line(
        donations_by_year,
        x='date',
        y='amount_normalized_total',
        title='Total Donated',
        x_title='',
        y_title='',
        hover='hover',
        dollars=True,
    )

    label = donations_by_year['num_donors'].tolist()[-1]
    label = f'<b>{last_year} Donors</b><br>{label:,} People'
    donations_by_year['label'] = label

    num_donors_graph = Line(
        donations_by_year,
        x='date',
        y='num_donors',
        title='Annual Number of Donors',
        x_title='',
        y_title='',
        hover='hover',
    )

    return html.Div(
        [
            html.Div(
                html.H2('Giving What We Can Donations'),
                className='section-heading',
            ),
            get_subtitle('gwwc_pledges', hover='points', zoom=True),
            html.Div(
                [
                    annual_donations_graph,
                    num_donors_graph,
                    total_donations_graph,
                ],
                className='grid tab-cols-3 desk-cols-3 section-body'
            ),
        ],
        className = 'section',
        id='gwwc-donations-section',
    )
