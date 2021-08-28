import dash_html_components as html
import dash_core_components as dcc

data_source_details = {

    'rethink19': dict(
        name='2019 Rethink Priorities Survey',
        url='https://www.rethinkpriorities.org/blog/2019/12/5/ea-survey-2019-series-community-demographics-amp-characteristics'
    ),

}

def get_subtitle(data_sources):

    if type(data_sources)==str:
        data_sources = [ data_sources ]

    data_links = [
        dcc.Link(
            data_source_details[data_source]['name'],
            href = data_source_details[data_source]['url']
        )
        for data_source in data_sources
    ]

    links_and_commas = [
        link_or_comma
        for link_and_comma in zip(data_links, [',']*len(data_links))
        for link_or_comma in link_and_comma
    ]
    links_and_commas = links_and_commas[:-1]

    return html.Div(
        [
            html.P( ['Data source: '] + links_and_commas + ['.'] ),
            html.P('Hover over the bars for more details.'),
            html.P('Click and drag to zoom. Double click to unzoom.'),
        ],
        className='section-subtitle',
    )


