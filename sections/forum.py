import plotly.express as px
import pandas as pd
import numpy as np
from dash import dcc
from dash import html
from dash import dash_table
from math import log
from plots.bar import Bar
from utils.subtitle import get_subtitle
from plots.scatter import Scatter
import json

def get_forum_data():

    with open('./data/forum.json', 'r') as forum_file:
        forum_json = json.loads(forum_file.read())

    posts = forum_json['data']['posts']['results']

    posts_df = pd.DataFrame(
        columns=['title', 'posted_at', 'authors', 'url', 'wordcount', 'karma', 'comments']
    )

    for post in posts:

        author_list = []
        try:
            author_list.append( post['user']['displayName'] )
        except:
            author_list.append('anonymous')
        for coauthor in post['coauthors']:
            author_list.append( coauthor['displayName'] )
        author_string = ', '.join(author_list)

        comment_count = post['commentCount']
        # resolve nulls to zero
        comment_count = comment_count if comment_count else 0

        wordcount = post['wordCount']
        # resolve nulls to zero
        wordcount = wordcount if wordcount else 0

        posts_df.loc[len(posts_df), :] = [
            post['title'],
            post['postedAt'],
            author_string,
            post['pageUrl'],
            wordcount,
            post['baseScore'],
            comment_count,
        ]

    posts_df['posted_at'] = pd.to_datetime(posts_df['posted_at'])#, format='%m/%Y')
    posts_df = posts_df.sort_values(by='posted_at', ascending=False)
    posts_df['posted_at_readable'] = posts_df['posted_at'].dt.strftime('%d %b %Y')
    posts_df['size'] = posts_df['wordcount'] + 1

    # hovertext
    def hover(row):

        title = row['title']
        posted_at = row['posted_at_readable']
        authors = row['authors']
        wordcount = row['wordcount']
        karma = row['karma']
        comments = row['comments']

        result = ''
        result += f"<b>{title}</b>"
        result += f"<br>{authors}"
        result += f"<br>Posted {posted_at}"
        result += f"<br>{karma} karma, {comments} comments"

        return result

    posts_df['hover'] = posts_df.apply(hover, axis=1)

    return posts_df


def org_bar_chart(op_grants):

    op_orgs = op_grants.groupby(by='Organization Name', as_index=False).sum()
    op_orgs = op_orgs.sort_values(by='Amount')
    op_orgs['x'] = op_orgs['Organization Name']
    # op_orgs['x'] = op_orgs['x'].apply(lambda x: x if len(x) < 30 else x[:27]+'...')
    op_orgs['y'] = op_orgs['Amount']
    op_orgs['text'] = op_orgs['Amount'].apply(lambda x: f'${x:,.0f}')

    # Some organization names get truncated to the same value.
    # This prevents that:
    for val in op_orgs['x'].unique():
        val_df = op_orgs[ op_orgs['x']==val ]
        for i in range(1, len(val_df)):
            index = val_df.iloc[i].name
            op_orgs.loc[index, 'x'] = op_orgs.loc[index, 'x'][:-3-i] + '...'

    def hover(row):
        org = row['Organization Name']
        amount = row['text']
        grants = row['grants']
        return f'<b>{org}</b><br>{grants} grants<br>{amount} total'
    op_orgs['hover'] = op_orgs.apply(hover, axis=1)

    op_orgs_truncated = op_orgs.iloc[len(op_orgs)-25:]

    return Bar(op_orgs_truncated, title='Top 30 Donee Organizations')


def cause_bar_chart(op_grants):

    op_causes = op_grants.groupby(by='Focus Area', as_index=False).sum()
    op_causes = op_causes.sort_values(by='Amount')
    op_causes['x'] = op_causes['Focus Area']
    op_causes['y'] = op_causes['Amount']
    op_causes['text'] = op_causes['Amount'].apply(lambda x: f'${x:,.0f}')

    def hover(row):
        area = row['Focus Area']
        amount = row['text']
        grants = row['grants']
        return f'<b>{area}</b><br>{grants} grants<br>{amount} total'
    op_causes['hover'] = op_causes.apply(hover, axis=1)

    height_per_bar = 25 if len(op_causes) > 10 else 28
    height = height_per_bar * len(op_causes) + 20
    return Bar(op_causes, height=height, title='Focus Areas')


def forum_scatter(forum_df):

    return Scatter(
        forum_df,
        id = "forum-scatter",
        x = "posted_at",
        y = "karma",
        x_title = "Publication Date",
        y_title = "Karma",
        title = "Forum Posts (log)",
        hover = 'hover',
    )


def forum_scatter_section():

    forum_df = get_forum_data()

    return html.Div(
        [
            html.Div(
                html.H2('Forum Posts by Publication Date and Karma'),
                className='section-title',
            ),
            get_subtitle('open_phil', hover='points', zoom=True),
            html.Div(
                [
                    html.Div(
                        forum_scatter(forum_df),
                        className='plot-container',
                    ),
                ],
                className='section-body'
            ),
        ],
        className = 'section',
        id='forum-scatter-section',
    )

def forum_leaderboard_section():

    op_grants = get_op_grants()

    return html.Div(
        [
            html.Div(
                html.H2('Open Philanthropy Grants by Focus Area and Donee Organization'),
                className='section-title',
            ),
            get_subtitle('open_phil'),
            html.Div(
                html.Div(
                    [
                        html.Div(
                            cause_bar_chart(op_grants),
                            className='plot-container',
                        ),
                        html.Div(
                            org_bar_chart(op_grants),
                            className='plot-container',
                        ),
                    ],
                    className='grid desk-cols-2 tab-cols-2',
                ),
                className='section-body'
            ),
        ],
        className = 'section',
        id='op-grants-categories',
    )
