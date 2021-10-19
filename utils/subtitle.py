from dash import html
from dash import dcc

data_source_details = {

    'rethink19': dict(
        name='EA Survey 2019',
        url='https://www.rethinkpriorities.org/blog/2019/12/5/ea-survey-2019-series-community-demographics-amp-characteristics'
    ),

    'rethink19-geo': dict(
        name='EA Survey 2019',
        url='https://rethinkpriorities.org/publications/eas2019-geographic-distribution-of-eas'
    ),


    'ea_forum': dict(
        name='EA Forum GraphQL',
        url='https://forum.effectivealtruism.org/graphiql'
    ),

    'open_phil': dict(
        name='OP Grants Database',
        url='https://www.openphilanthropy.org/giving/grants'
    ),

    'funds_payout': dict(
        name='EA Funds Payout Reports',
        url='https://funds.effectivealtruism.org/'
    ),

    'founders_pledge': dict(
        name='Founders Pledge Homepage',
        url='https://founderspledge.com/'
    ),

    'gwwc': dict(
        name='GWWC Homepage',
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
        html.A(
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

    content.append([])

    if hover:
        content[-1].append( f'Hover for more details.' )

    if zoom:
        content[-1].append( 'Click and drag to zoom. Double click to unzoom.' )

    content[-1].extend(
        [
            text
            for text in extra_text
        ]
    )

    content[-1] = ' '.join(content[-1])

    return html.Div(
        content,
        className='section-subtitle',
    )


