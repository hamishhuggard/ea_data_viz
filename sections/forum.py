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

posts_df = None
def get_forum_data():
    global posts_df

    if type(posts_df) != type(None):
        return posts_df

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

    # remove very low karma posts
    posts_df = posts_df.loc[ posts_df['karma'] > -20 ]

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
    forum_df['posted_at'] = forum_df['posted_at'].dt.date
    forum_df['cumulative_word_count'] = forum_df['wordcount'].cumsum()

    authors = set()
    def new_authors(author_string):
        author_list = author_string.split(',')
        author_list = [ author.strip() for author in author_list ]
        new_authors = []
        for author in author_list:
            if author not in authors:
                new_authors.append(author)
                authors.add(author)
        return new_authors

    forum_df['new_authors'] = forum_df['authors'].apply(new_authors)
    forum_df['new_author_count'] = forum_df['new_authors'].apply(len)
    forum_df['author_count'] = forum_df['new_author_count'].cumsum()

    posted_at_groups = forum_df.groupby('posted_at')
    forum_by_day_df = pd.DataFrame({
        'posted_at': forum_df['posted_at'].unique(),
        'posted_at_readable': forum_df['posted_at_readable'].unique(),
    })

    # new posts

    forum_by_day_df['titles'] = posted_at_groups['title'].apply(list).tolist()
    forum_by_day_df['new_posts'] = posted_at_groups['Unit'].sum().tolist()
    forum_by_day_df['total_posts'] = posted_at_groups['Count'].last().tolist()

    label = forum_df['Count'].tolist()[-1]
    label = f'{label:,} Posts'
    forum_by_day_df['new_posts_label'] = label

    def new_posts_hover(row):

        new_posts = row['new_posts']
        total_posts = row['total_posts']
        posted_at = row['posted_at_readable']
        titles = row['titles']

        max_displayed_titles = 10
        if len(titles) > max_displayed_titles:
            titles = titles[:max_displayed_titles] + ['...']

        result = ''
        result += f"<b>{posted_at}</b>"
        result += f"<br><b>{new_posts} new posts ({total_posts:,} total):</b>"
        for title in titles:

            max_title_length = 50
            if len(title) > max_title_length:
                title = title[:max_title_length] + '...'
            result += f"<br>{title}"

        return result

    forum_by_day_df['new_posts_hover'] = forum_by_day_df.apply(new_posts_hover, axis=1)


    # new authors

    forum_by_day_df['new_authors'] = posted_at_groups['new_authors'].sum().tolist()
    forum_by_day_df['new_author_count'] = posted_at_groups['new_author_count'].sum().tolist()
    forum_by_day_df['author_count'] = posted_at_groups['author_count'].last().tolist()

    label = forum_df['author_count'].tolist()[-1]
    label = f'{label:,} Unique Authors'
    forum_by_day_df['new_authors_label'] = label

    def new_authors_hover(row):

        new_authors = row['new_authors']
        new_authors_count = row['new_author_count']
        total_authors = row['author_count']
        posted_at = row['posted_at_readable']

        max_displayed_authors = 10
        if len(new_authors) > max_displayed_authors:
            new_authors = new_authors[:max_displayed_authors] + ['...']

        result = ''
        result += f"<b>{posted_at}</b>"
        result += f"<br><b>{new_authors_count} new authors ({total_authors:,} total):</b>"
        for author in new_authors:

            max_author_length = 50
            if len(author) > max_author_length:
                author = author[:max_author_length] + '...'
            result += f"<br>{author}"

        return result

    forum_by_day_df['new_authors_hover'] = forum_by_day_df.apply(new_authors_hover, axis=1)


    # word count


    forum_by_day_df['new_words'] = posted_at_groups['wordcount'].sum().tolist()
    forum_by_day_df['total_words'] = posted_at_groups['cumulative_word_count'].last().tolist()

    label = forum_by_day_df['total_words'].tolist()[-1]
    label = f'{label:,} Words'
    forum_by_day_df['word_count_label'] = label

    def word_count_hover(row):

        new_words = row['new_words']
        total_words = row['total_words']
        posted_at = row['posted_at_readable']

        result = ''
        result += f"<b>{posted_at}</b>"
        result += f"<br>{total_words:,} total words"
        result += f"<br>{new_words:,} new words"

        return result

    forum_by_day_df['word_count_hover'] = forum_by_day_df.apply(word_count_hover, axis=1)



    # New posts line plot

    post_count_graph = Line(
        forum_by_day_df,
        x='posted_at',
        y='total_posts',
        x_title = '',
        y_title = '',
        hover = 'new_posts_hover',
        title = 'Post Count',
        label = 'new_posts_label',
    )

    # New authors line plot

    unique_authors_df = forum_by_day_df.loc[ forum_by_day_df['new_author_count'] > 0 ]

    author_count_graph = Line(
        unique_authors_df,
        x='posted_at',
        y='author_count',
        x_title = '',
        y_title = '',
        hover = 'new_authors_hover',
        title = 'Unique Author Count',
        label = 'new_authors_label',
    )



    # New words line plot

    new_words_df = forum_by_day_df.loc[ forum_by_day_df['new_words'] > 0 ]

    word_count_graph = Line(
        new_words_df,
        x='posted_at',
        y='total_words',
        x_title = '',
        y_title = '',
        hover = 'word_count_hover',
        title = 'Cumulative Word Count',
        label = 'word_count_label',
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
