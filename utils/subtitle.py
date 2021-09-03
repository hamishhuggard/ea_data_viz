import dash_html_components as html
import dash_core_components as dcc

data_source_details = {

    'rethink19': dict(
        name='EA Survey 2019 (Rethink Priorities)',
        url='https://www.rethinkpriorities.org/blog/2019/12/5/ea-survey-2019-series-community-demographics-amp-characteristics'
    ),

    'rethink19-geo': dict(
        name='EA Survey 2019 (Rethink Priorities)',
        url='https://rethinkpriorities.org/publications/eas2019-geographic-distribution-of-eas'
    ),


    'open_phil': dict(
        name='Open Philanthropy Grants Database',
        url='https://www.openphilanthropy.org/giving/grants'
    ),

    'funds_payout': dict(
        name='Effective Altruism Funds Payout Reports',
        url='https://funds.effectivealtruism.org/'
    ),

    'founders_pledge': dict(
        name='Founders Pledge Homepage',
        url='https://founderspledge.com/'
    ),

    'gwwc': dict(
        name='Giving What We Can Homepage',
        url='https://www.givingwhatwecan.org/'
    ),

    'growth': dict(
        name='EA Growth Metrics for 2018',
        url='https://forum.effectivealtruism.org/posts/MBJvDDw2sFGkFCA29/is-ea-growing-ea-growth-metrics-for-2018',
    ),

}

def get_subtitle(data_sources, zoom=False, hover='bars', extra_text=[]):

    if type(data_sources)==str:
        data_sources = [ data_sources ]

    if type(extra_text)==str:
        extra_text = [ extra_text ]

    data_links = [
        dcc.Link(
            data_source_details[data_source]['name'],
            href = data_source_details[data_source]['url']
        )
        for data_source in data_sources
    ]

    links_and_commas = [
        link_or_comma
        for link_and_comma in zip(data_links, [', ']*len(data_links))
        for link_or_comma in link_and_comma
    ]
    links_and_commas = links_and_commas[:-1]

    content = []

    if len(data_sources) > 0:
        content.append(
            html.P( ['Data source: '] + links_and_commas + ['.'] ),
        )

    if hover:
        content.append(
            html.P(f'Hover over the {hover} for more details.'),
        )

    if zoom:
        content.append(
            html.P('Click and drag to zoom. Double click to unzoom.'),
        )

    content.extend(
        [
            html.P(text)
            for text in extra_text
        ]
    )

    return html.Div(
        content,
        className='section-subtitle',
    )


