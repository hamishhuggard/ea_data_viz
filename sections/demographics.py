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
    # demo_table['label'] = demo_table[title] + demo_table['Percent']
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))



    subs = {
        'Eat meat, but try to reduce the amount  ': 'Reducetarian',
    #     # 'Eat meat': 'Meat',
    #     # 'Vegetarian': 'Veg.',
    #     # 'Pescetarian': 'Pesc.',
        'Other (please specify)': 'Other',

        'Native Hawaiian or Other Pacific Islander': 'Hawaiian or Pacific Islander',
        'American Indian or Alaskan Native': 'Native American/Alaskan', 
    #     'Black or African American': 'Black',
        'Hispanic, Latino or Spanish Origin': 'Hispanic or Latino',

    #     # 'Computer Science': 'CS',
    #     'Math': 'Math',
    #     # 'Economics': 'Econ',
    #     # 'Social Science': 'Soc. Sci.',
    #     # 'Philosophy': 'Phil',
    #     # 'Psychology': 'Science',#'Psych',
    #     # 'Arts & Humanities': 'Arts',
    #     # 'Sciences': 'Other',
    #     # 'Engineering': 'Other',
    #     # 'Physics': 'Other',
    #     # 'Psychology': 'Other',
    #     # 'Medicine': 'Other',
        'Professional or vocational qualification': 'Professional or Vocational',

    #     'Employed, Full-Time': 'Employed (FT)',
    #     'Student, Full-Time': 'Student (FT)',
    #     'Employed, Part-Time': 'Employed (PT)',
        'Not employed, but looking for work': 'Not employed, looking for work',
    #     'Student, Part-Time': 'Student (PT)',
        'Not employed, but not looking for work': 'Not employed, not looking for work',
    #     # 'Homemaker ': 'Other',
    #     # 'Student, Part-Time': 'Student',
    #     # 'Self-Employed': 'Self-Employ',

        'Work at a non-profit (not an EA organization)': 'Non-profit (not EA org)',
        'Work at a non-profit (EA organization)': 'Non-profit (EA org)',


        'Consequentialism (utilitarian)': 'Utilitarianism',
        'Consequentualism (other than utilitarian)': 'Other Consequentialism',

    #     # '13-17': '13-17'
    #     # 18-24
    #     # 25-34
    #     # 35-44
    #     # 45-54
    #     # 55-64
    #     # 65+
    }
    # max_chars = 20
    demo_table['label'] = demo_table[title].map(subs).fillna(demo_table[title])
    # demo_table['label'] = demo_table['label'].apply(lambda x: x.rjust(max_chars))

    # swap utilitarianism and consequentialism in the moral_belief table
    if title == 'Moral View':
        demo_table = demo_table.loc[[ 1, 0, 2, 3, 4 ], :]

    # # Normalise title
    # title_subs = {
    #     'Age Group': 'Age',
    #     'Employment Type': 'Employment',
    #     'Race/Ethnicity': 'Ethnicity',
    #     'Subject Studied': 'Subject Studied',
    #     'Moral View': 'Moral View',
    #     'Gender': 'Gender',
    #     'Diet ': 'Diet',
    #     'Education': 'Education',
    #     'Career path': 'Career path' 
    # }
    # title = title_subs[title]

    return demo_table

pad_to = len('Hawaiian or Pacific Islander') + 8

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

        demo_table['label'] = demo_table['label'] + demo_table['Percent'].apply(lambda x: f'{x:>8}%')
        demo_table['label'] = demo_table['label'].apply(lambda x: ('{:>'+str(pad_to)+'}').format(x))
        demo_table['x'] = demo_table['label']
        demo_table['y'] = demo_table['Percent']

        bar = EABarGraph(demo_table, height, title)
        bars.append(
            html.Div(
                bar,
                className='demo-column',
                style={
                    'width': width
                }
            )
        )

    return bars

content = html.Div(
    [
        html.Div(
            [
                html.Div(
                    html.H2('Demographics and Beliefs'),
                    className='section-heading',
                ),
                # html.P('Hover over the bars for more details.'),
                html.P([
                    'Data source: ',
                    dcc.Link(
                        '2019 Rethink Priorities Survey',
                        href='https://www.rethinkpriorities.org/blog/2019/12/5/ea-survey-2019-series-community-demographics-amp-characteristics'
                    ),
                ]),
            ] + \
#        html.P(
#            'There are about {} active members of the '.format(6500) + \
#            'Effective Altruism community. Who are they?'
#            # source: https://www.rethinkpriorities.org/blog/2020/6/26/ea-survey-2019-series-how-many-people-are-there-in-the-ea-community
            create_row(
                ['gender', 'age_group', 'ethnicity'],
                ['32.5%', '32.5%', '35%']
            ) + \
        #     ),
        #     style={'overflow': 'auto'}
        # ),

        # html.Div(
            create_row(
                ['political_belief', 'diet', 'moral_view', ],
                ['32.5%', '32.5%', '35%']
        #     ) + \
            ),
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
            ] + \
            create_row(
                ['education2', 'career_path']
            ) + \
            create_row(
                ['subject', 'employment'],
            ),
            className = 'section',
        ),

    ],
)

