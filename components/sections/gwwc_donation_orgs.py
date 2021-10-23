import pandas as pd
from dash import html
from utils.subtitle import get_subtitle
from utils.plots.bar import Bar
from utils.get_data.query_gwwc import get_donations_by_org

def get_hover(row):

    amount = row['Amount (USD)']

    result = ''
    result += f"<b>{row.Organisation}</b>"
    result += f"<br>${amount:,.2f} donated"
    result += f"<br>{row.Donors} donors"
    result += f"<br>{row.Donations} donations"

    return result

def get_top_orgs_by_amount(donations_by_org):
    donations_by_org = donations_by_org.sort_values(by='Amount (USD)', ascending=False)
    donations_by_org = donations_by_org.reset_index()
    donations_by_org = donations_by_org.iloc[:20]
    donations_by_org = donations_by_org.iloc[::-1]
    donations_by_org['y'] = donations_by_org['Amount (USD)']
    donations_by_org['x'] = donations_by_org['Organisation']
    donations_by_org['hover'] = donations_by_org.apply(get_hover, axis=1)
    donations_by_org['text'] = donations_by_org['Amount (USD)'].apply(lambda x: f'${x:,.2f}')
    return Bar(donations_by_org, title='Top Organizations by Amount')

def get_top_orgs_by_num_donors(donations_by_org):
    donations_by_org = donations_by_org.sort_values(by='Donors', ascending=False)
    donations_by_org = donations_by_org.reset_index()
    donations_by_org = donations_by_org.iloc[:20]
    donations_by_org = donations_by_org.iloc[::-1]
    donations_by_org['y'] = donations_by_org['Donors']
    donations_by_org['x'] = donations_by_org['Organisation']
    donations_by_org['hover'] = donations_by_org.apply(get_hover, axis=1)
    donations_by_org['text'] = donations_by_org['Donors'].apply(lambda x: f'{x:,}')
    return Bar(donations_by_org, title='Top Organizations by Number of Donors')


def get_gwwc_donations_orgs_section():

    donations_by_org = pd.read_json('./data/gwwc/donations_by_org.json')
    #donations_by_org = get_donations_by_org()

    return html.Div(
        [
            html.Div(
                html.H2('Giving What We Can Donations by Organization'),
                className='section-heading',
            ),
            get_subtitle('gwwc_orgs', hover='points', zoom=True),
            html.Div(
                [
                    get_top_orgs_by_amount(donations_by_org),
                    get_top_orgs_by_num_donors(donations_by_org),
                ],
                className='grid tab-cols-2 desk-cols-2 section-body'
            ),
        ],
        className = 'section',
        id='gwwc-orgs-section',
    )
