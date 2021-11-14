from dash import html
from dash import dcc

data_source_details = {

    'rethink19': dict(
        name='EA Survey 2019',
        url='https://www.rethinkpriorities.org/blog/2019/12/5/ea-survey-2019-series-community-demographics-amp-characteristics'
    ),

    'rethink19-geo': dict(
        name='EA Survey 2019',
        url='https://rethinkpriorities.org/publications/eas2019-geographic-distribution-of-eas',
        download_url='/assets/data/rp_survey_data_2019/country2.csv'
    ),

    'ea_forum': dict(
        name='forum.effectivealtruism.org',
        url='https://forum.effectivealtruism.org/graphiql',
    ),

    'open_phil': dict(
        name='openphilanthropy.org',
        url='https://www.openphilanthropy.org/giving/grants',
        download_url='https://www.openphilanthropy.org/giving/grants/spreadsheet',
    ),

    'funds_payout': dict(
        name='funds.effectivealtruism.org',
        url='https://funds.effectivealtruism.org/'
    ),

    'founders_pledge': dict(
        name='founderspledge.com',
        url='https://founderspledge.com/'
    ),

    'gwwc': dict(
        name='givingwhatwecan.org',
        url='https://www.givingwhatwecan.org/'
    ),

    'growth': dict(
        name='EA Growth Metrics for 2018',
        url='https://forum.effectivealtruism.org/posts/MBJvDDw2sFGkFCA29/is-ea-growing-ea-growth-metrics-for-2018',
    ),

    'gwwc_pledges': dict(
        name='dashboard.effectivealtruism.org',
        url='http://dashboard.effectivealtruism.org/public/question/a8499095-be16-46fe-af1f-e3e56ee04e88',
    ),

    'gwwc_donations': dict(
        name='dashboard.effectivealtruism.org',
        url='http://dashboard.effectivealtruism.org/public/question/9906735e-1350-4353-9828-bb3ec16137e3',
    ),

    'gwwc_orgs': dict(
        name='dashboard.effectivealtruism.org',
        url='http://dashboard.effectivealtruism.org/public/question/b3887098-686a-491c-9f9c-9a5b0e2b7fd8',
    ),

}

def get_data_source(data_sources):

    if len(data_sources) == 0:
        return html.Div()

    if type(data_sources)==str:
        data_sources = [ data_sources ]


    content = [ 'Data source: ' ]

    list_of_source_links = []
    for data_source in data_sources:

        details = data_source_details[data_source]

        content.append(
            html.A(
                details['name'],
                href = details['url']
            )
        )

        # download link
        if 'download_url' in details:
            content.append(' (')
            content.append(
                html.A(
                    'download',
                    href = details['download_url'],
                )
            )
            content.append(')')

        content.append(', ')

    # Change the last comma into a period.
    content[-1] = '.'

    return html.P(content)

def get_instructions(zoom=False, hover='bars', extra_text=[]):

    content = []

    if hover:
        content.append( f'Hover for more details.' )

    if zoom:
        content.append( 'Click and drag to zoom. Double click to unzoom.' )

    if type(extra_text)==str:
        content.append(extra_text)
    elif type(extra_text)==list:
        content.extend(extra_text)

    return html.P(' '.join(content))


