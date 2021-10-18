from dash import dcc
from dash import html
from dash import dash_table

import pandas as pd
import numpy as np

from math import log
from utils.subtitle import get_subtitle
import json

from plots.bar import Bar
from plots.line import Line
from plots.scatter import Scatter

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
