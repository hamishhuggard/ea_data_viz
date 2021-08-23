import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import re
from glob import glob
from utils.ea_bar_graph import EABarGraph

##################################
###       DEMOGRAPHICS         ###
##################################

def get_demo_table(demo_name):

    path = f"./data/rp_survey_data/{demo_name}.csv"
    demo_table = pd.read_csv(path, sep='\t')
    title = demo_table.columns[0]

    # remove the 'Total' row
    demo_table = demo_table[ ~demo_table[title].isin(['Total', 'Total respondents']) ]
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))



    # Substitute the long labels for something shorter
    subs = {
        'Eat meat, but try to reduce the amount  ': 'Reducetarian',
        'Other (please specify)': 'Other',

        'Native Hawaiian or Other Pacific Islander': 'Hawaiian or Pacific Islander',
        'American Indian or Alaskan Native': 'Native American/Alaskan',
        'Hispanic, Latino or Spanish Origin': 'Hispanic or Latino',

        'Professional or vocational qualification': 'Professional or Vocational',

        'Not employed, but looking for work': 'Not employed, looking for work',
        'Not employed, but not looking for work': 'Not employed, not looking for work',

        'Work at a non-profit (not an EA organization)': 'Non-profit (not EA org)',
        'Work at a non-profit (EA organization)': 'Non-profit (EA org)',


        'Consequentialism (utilitarian)': 'Utilitarianism',
        'Consequentualism (other than utilitarian)': 'Other Consequentialism',
    }
    demo_table['label_original'] = demo_table[title]
    demo_table['label'] = demo_table[title].map(subs).fillna(demo_table[title])

    if title == 'Moral View':
        demo_table = demo_table.loc[[ 4, 2, 3, 1, 0, ], :]

    return demo_table

def create_row(demo_names, widths=None):

    if not widths:
        widths = [ f'{100/len(demo_names)}%' ] * len(demo_names)

    demo_tables = []
    demo_heights = []

    for demo_name in demo_names:

        demo_table = get_demo_table(demo_name)
        demo_tables.append(demo_table)

        height_per_bar = 25 if len(demo_table) > 10 else 28
        height = height_per_bar * len(demo_table) + 30
        demo_heights.append(height)

    height = max(demo_heights)
    bars = []

    for width, demo_table in zip(widths, demo_tables):

        title = demo_table.columns[0]
        demo_table['x'] = demo_table['label']
        demo_table['y'] = demo_table['Percent']
        demo_table['text'] = demo_table['Percent'].apply(lambda x: f'{x:.1f}%')

        def hover(row):
            label = row['label_original']
            responses = row['Responses']
            percent = row['Percent']
            return f'<b>{label}</b><br>{responses} responses ({percent}%)'

        demo_table['hover'] = demo_table.apply(hover, axis=1)

        bar = EABarGraph(demo_table, height, title)
        bars.append(
            html.Div(
                bar,
                className='demographics-panel',
            )
        )

    return bars

class Demographics(html.Div):
    def __init__(self):
        super(Demographics, self).__init__(
            [
                html.Div(
                    [
                        html.Div(
                            html.H2('Demographics and Beliefs'),
                            className='section-heading',
                        ),
                        html.P([
                            'Data source: ',
                            dcc.Link(
                                '2019 Rethink Priorities Survey',
                                href='https://www.rethinkpriorities.org/blog/2019/12/5/ea-survey-2019-series-community-demographics-amp-characteristics'
                            ),
                            '. Hover over the bars for more details.',
                        ]),
                        html.Div(
                            html.Div(
                                create_row(
                                    ['gender', 'age_group', 'ethnicity'],
                                    ['32.5%', '32.5%', '35%']
                                ) + \
                                create_row(
                                    ['political_belief', 'diet', 'moral_view', ],
                                    ['32.5%', '32.5%', '35%']
                                ),
                                className = 'demographics-container grid-1-cols grid-2-cols grid-3-cols',
                            )
                        )
                    ],
                    className = 'section',
                ),

                html.Div(
                    [
                        html.Div(
                            html.H2('Education and Career'),
                            className='section-heading',
                        ),
                        html.P([
                            'Data source: ',
                            dcc.Link(
                                '2019 Rethink Priorities Survey',
                                href='https://www.rethinkpriorities.org/blog/2019/12/5/ea-survey-2019-series-community-demographics-amp-characteristics'
                            ),
                        ]),
                        html.Div(
                            html.Div(
                                create_row(
                                    ['education2', 'career_path']
                                ) + \
                                create_row(
                                    ['subject', 'employment'],
                                ),
                                className = 'demographics-container grid-1-cols grid-2-cols',
                            )
                        )
                    ],
                    className = 'section',
                ),

            ],
        )
