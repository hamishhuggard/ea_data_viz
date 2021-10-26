from dash import html
import pandas as pd
from utils.subtitle import get_data_source
from utils.subtitle import get_instructions
from utils.plots.line import Line
from utils.get_data.query_gwwc import get_new_pledges


def get_the_pledge_hover(row):

    date = row['date'].strftime('%B %Y')
    new_pledges = row['the_pledge']
    total_pledges = row['the_pledge_total']

    result = ''
    result += f"<b>GWWC Pledges</b>"
    result += f"<br><b>{date}</b>"
    result += f"<br>{new_pledges:,} new pledges"
    result += f"<br>{total_pledges:,} total pledges"

    return result


def get_try_giving_hover(row):

    date = row['date'].strftime('%B %Y')
    new_pledges = row['try_giving']
    total_pledges = row['try_giving_total']

    result = ''
    result += f"<b>Trial Pledges</b>"
    result += f"<br><b>{date}</b>"
    result += f"<br>{new_pledges:,} new pledges"
    result += f"<br>{total_pledges:,} total pledges"

    return result


def get_new_pledges_long(new_pledges):

    new_pledges_long = new_pledges.loc[:, ['date']]
    new_pledges_long['value'] = new_pledges['the_pledge']
    new_pledges_long['hover'] = new_pledges['the_pledge_hover']

    label = new_pledges_long['value'].tolist()[-1]
    last_date = new_pledges_long['date'].tolist()[-1]
    last_year = last_date.strftime('%Y')
    last_month = last_date.strftime('%B')
    new_pledges_long['label'] = f'<b>{label:,} New</b><br>{last_month}<br>{last_year}'

    return new_pledges_long

def get_new_trial_pledges_long(new_pledges):

    new_try_giving_long = new_pledges.loc[:, ['date']]
    new_try_giving_long['value'] = new_pledges['try_giving']
    new_try_giving_long['hover'] = new_pledges['try_giving_hover']

    label = new_try_giving_long['value'].tolist()[-1]
    last_date = new_try_giving_long['date'].tolist()[-1]
    last_year = last_date.strftime('%Y')
    last_month = last_date.strftime('%B')
    new_try_giving_long['label'] = f'<b>{label:,} New</b><br>{last_month}<br>{last_year}'

    return new_try_giving_long



def get_total_pledges_long(new_pledges):

    total_pledges_long = new_pledges.loc[:, ['date']]
    total_pledges_long['value'] = new_pledges['the_pledge_total']
    total_pledges_long['hover'] = new_pledges['the_pledge_hover']

    label = total_pledges_long['value'].tolist()[-1]
    #last_date = int(total_pledges_long['date'].tolist()[-1])
    total_pledges_long['label'] = f'<b>{label:,}</b><br>Giving Pledges'

    total_try_giving_long = new_pledges.loc[:, ['date']]
    total_try_giving_long['value'] = new_pledges['try_giving_total']
    total_try_giving_long['hover'] = new_pledges['try_giving_hover']

    label = total_try_giving_long['value'].tolist()[-1]
    #last_date = int(total_try_giving_long['date'].tolist()[-1])
    total_try_giving_long['label'] = f'<b>{label:,}</b><br>Trial Pledges'

    return pd.concat([total_pledges_long, total_try_giving_long], ignore_index=True)


def get_gwwc_pledges_section():

    new_pledges = pd.read_json('./data/gwwc/new_pledges.json')
    #new_pledges = get_new_pledges()

    new_pledges['date'] = pd.to_datetime(new_pledges['pledge_month'])

    new_pledges['the_pledge_total'] = new_pledges['the_pledge'].cumsum()
    new_pledges['try_giving_total'] = new_pledges['try_giving'].cumsum()

    new_pledges['the_pledge_hover'] = new_pledges.apply(get_the_pledge_hover, axis=1)
    new_pledges['try_giving_hover'] = new_pledges.apply(get_try_giving_hover, axis=1)

    new_pledges_long = get_new_pledges_long(new_pledges)
    new_trial_pledges_long = get_new_trial_pledges_long(new_pledges)
    total_pledges_long = get_total_pledges_long(new_pledges)

    new_pledges_graph = Line(
        new_pledges_long,
        x='date',
        y='value',
        title='New Giving Pledges by Month',
        x_title='',
        y_title='',
        xanchor='left',
        yanchor='middle',
    )

    new_trial_pledges_graph = Line(
        new_trial_pledges_long,
        x='date',
        y='value',
        title='New Trial Pledges by Month',
        x_title='',
        y_title='',
        xanchor='left',
        yanchor='middle',
    )

    total_pledges_graph = Line(
        total_pledges_long,
        x='date',
        y='value',
        title='Total Pledges',
        x_title='',
        y_title='',
        xanchor='center',
    )

    return html.Div(
        [
            html.Div(
                html.H2('Giving What We Can Pledges'),
                className='section-heading',
            ),
            get_instructions(hover='points', zoom=True),
            html.Div(
                [
                    new_pledges_graph,
                    new_trial_pledges_graph,
                    total_pledges_graph
                ],
                className='grid desk-cols-3 section-body'
            ),
            get_data_source('gwwc_pledges'),
        ],
        className = 'section',
        id='gwwc-pledge-section',
    )
