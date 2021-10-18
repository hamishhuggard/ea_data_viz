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
        title = "",
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
        id='forum-cumulative-section',
    )

def post_counts(forum_df):


    forum_df = forum_df.sort_values(by='posted_at')

    forum_df['Unit'] = 1
    forum_df['Count'] = forum_df['Unit'].cumsum()
    label = forum_df['Count'].tolist()[-1]
    label = f'{label:,} Posts'
    forum_df['label'] = label

    forum_df['posted_at'] = forum_df['posted_at'].dt.date
    posted_at_groups = forum_df.groupby('posted_at')
    post_counts_df = pd.DataFrame({
        'posted_at': forum_df['posted_at'].unique()
    })
    #titles_string = posted_at_groups['title'].transform(lambda x: ', '.join(x))
    #titles_string = titles_string.drop_duplicates().tolist()
    #post_counts_df['titles'] = titles_string
    post_counts_df['titles'] = posted_at_groups['title'].apply(list).tolist()
    post_counts_df['new_posts'] = posted_at_groups['Unit'].sum().tolist()
    post_counts_df['new_words'] = posted_at_groups['wordcount'].sum().tolist()
    post_counts_df['total_posts'] = posted_at_groups['Count'].last().tolist()
    print(post_counts_df)

    def hover(row):

        title = row['title']
        posted_at = row['posted_at_readable']
        wordcount = row['wordcount']
        karma = row['karma']
        comments = row['comments']

        result = ''
        result += f"<b>{title}</b>"
        result += f"<br>{authors}"
        result += f"<br>Posted {posted_at}"
        result += f"<br>{karma} karma, {comments} comments"

        return result

    #forum_df['hover'] = forum_df.apply(hover, axis=1)

    post_count_graph = Line(
        forum_df,
        x='posted_at',
        y='Count',
        x_title = '',
        y_title = '',
        hover = 'hover',
        title = 'Post Count',
    )

    authors = set()
    def new_authors(author_string):
        author_list = author_string.split(',')
        author_list = [ author.strip() for author in author_list ]
        authors_before = len(authors)
        authors.update(author_list)
        authors_after = len(authors)
        return authors_after - authors_before
    forum_df['new_authors'] = forum_df['authors'].apply(new_authors)
    forum_df['author_count'] = forum_df['new_authors'].cumsum()
    label = forum_df['author_count'].tolist()[-1]
    label = f'{label:,} Unique Authors'
    forum_df['label'] = label

    author_count_graph = Line(
        forum_df,
        x='posted_at',
        y='author_count',
        x_title = '',
        y_title = '',
        hover = 'hover',
        title = 'Unique Author Count',
    )

    forum_df['cumulative_word_count'] = forum_df['wordcount'].cumsum()
    label = forum_df['cumulative_word_count'].tolist()[-1]
    label = f'{label:,} Words'
    forum_df['label'] = label

    word_count_graph = Line(
        forum_df,
        x='posted_at',
        y='cumulative_word_count',
        x_title = '',
        y_title = '',
        hover = 'hover',
        title = 'Cumulative Word Count',
    )

    return [
        post_count_graph,
        author_count_graph,
        word_count_graph,
    ]

def forum_count_section():

    forum_df = get_forum_data()

    post_count_graph, author_count_graph, word_count_graph = post_counts(forum_df)

    return html.Div(
        [
            html.Div(
                html.H2('Cumulative Writing on EA Forum'),
                className='section-title',
            ),
            get_subtitle('open_phil', hover='points', zoom=True),
            html.Div(
                [
                    html.Div(
                        post_count_graph,
                        className='plot-container',
                    ),
                    html.Div(
                        author_count_graph,
                        className='plot-container',
                    ),
                    html.Div(
                        word_count_graph,
                        className='plot-container',
                    ),
                ],
                className='grid tab-cols-2 desk-cols-3 section-body'
            ),
        ],
        className = 'section',
        id='forum-scatter-section',
    )

def forum_post_wilkinson_section():
    return html.Div()

def forum_user_wilkinson_section():
    html.Div()
