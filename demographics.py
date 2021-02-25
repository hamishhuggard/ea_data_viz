import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import re
from glob import glob
from ea_bar_graph import EABarGraph

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

def create_row(demo_names, widths=None):

    if not widths:
        widths = [ f'{95/len(demo_names)}%' ] * len(demo_names)

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

demo_names = [
        'gender',
        'ethnicity',
        'age_group',
        'education2',
        'subject',
        'career_path',
        'employment',
        'political_belief',
        'diet',
        'moral_view',
]

demo_bars = {
    demo_name: get_demo_table(demo_name)
    for demo_name in demo_names
}

demo_div = html.Div(
    [
        html.Div(
            [
                html.Div(
                    # html.H2('Demographics'),
                    html.H2('Demographics, Backgrounds, Beliefs'),
                    className='section-heading',
                ),
            ] + create_row(
                ['gender', 'age_group', 'ethnicity'],
                ['27%', '27%', '38%']
            ),
            #    html.Div(
            #        demo_bars['gender'],
            #        className='demo-column',
            #        style={
            #            'width': '27%'
            #        }
            #    ),
            #    html.Div(
            #        demo_bars['age_group'],
            #        className='demo-column',
            #        style={
            #            'width': '27%'
            #        }
            #    ),
            #    html.Div(
            #        demo_bars['ethnicity'],
            #        className='demo-column',
            #        style={
            #            'width': '38%'
            #        }
            #    ),
            #],
            style={'overflow': 'auto'}
        ),

        html.Div(
            create_row(
                ['education2', 'subject']
            ),
            #[
            #    # html.Div(
            #    #     html.H2('Education'),
            #    #     className='section-heading',
            #    # ),
            #    html.Div(
            #        demo_bars['education2'],
            #        className='demo-column',
            #        style={
            #            'width': '45%'
            #        }
            #    ),
            #    html.Div(
            #        demo_bars['subject'],
            #        className='demo-column',
            #        style={
            #            'width': '45%'
            #        }
            #    ),
            #],
            style={'overflow': 'auto'}
        ),

        html.Div(
            create_row(
                ['career_path', 'employment'],
            ),
            #[
            #    # html.Div(
            #    #     html.H2('Career'),
            #    #     className='section-heading',
            #    # ),
            #    html.Div(
            #        demo_bars['career_path'],
            #        className='demo-column',
            #        style={
            #            'width': '45%'
            #        }
            #    ),
            #    html.Div(
            #        demo_bars['employment'],
            #        className='demo-column',
            #        style={
            #            'width': '45%'
            #        }
            #    ),
            #],
            style={'overflow': 'auto'}
#            className='big-box'
        ),

        html.Div(
            create_row(
                ['political_belief', 'moral_view', 'diet'],
                ['30%', '35%', '30%']
            ),
            #[
            #    # html.Div(
            #    #     html.H2('Beliefs'),
            #    #     className='section-heading',
            #    # ),
            #    html.Div(
            #        demo_bars['political_belief'],
            #        className='demo-column',
            #        style={
            #            'width': '30%'
            #        }
            #    ),
            #    html.Div(
            #        demo_bars['moral_view'],
            #        className='demo-column',
            #        style={
            #            'width': '30%'
            #        }
            #    ),
            #    html.Div(
            #        demo_bars['diet'],
            #        className='demo-column',
            #        style={
            #            'width': '30%'
            #        }
            #    ),
            #],
            style={'overflow': 'auto'}
#            className='big-box'
        ),





#        html.P(
#            'There are about {} active members of the '.format(6500) + \
#            'Effective Altruism community. Who are they?'
#            # source: https://www.rethinkpriorities.org/blog/2020/6/26/ea-survey-2019-series-how-many-people-are-there-in-the-ea-community
#        ),
#        html.Div(
#            [
#                demo_bars['gender'],
#                demo_bars['age_group'],
#                demo_bars['ethnicity'],
#
#            ],
#            className='demo-column',
#            style = {
#                # 'background-color': 'yellow',
#            }
#        ),
#
#        html.Div(
#            [
#                demo_bars['diet'],
#                demo_bars['employment'],
#            ],
#            className='demo-column',
#            style = {
#                # 'background-color': 'red',
#            }
#        ),
#
#        html.Div(
#            [
#                demo_bars['subject'],
#                demo_bars['education2'],
#            ],
#            className='demo-column',
#            # style = {
#            #     # 'background-color': 'yellow',
#            # }
#        ),
#        html.Div(
#            [
#                demo_bars['moral_view'],
#            ],
#            className='demo-column',
#            # style = {
#            #     # 'background-color': 'yellow',
#            # }
#        ),


    ],
#    className='big-box'
)
