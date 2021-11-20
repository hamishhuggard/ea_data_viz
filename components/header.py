# -*- coding: utf-8 -*-

import dash
from dash import dcc
from dash import html
import dash_dangerously_set_inner_html
import visdcc

def header():

    lightbulb_img_url = '/assets/logo.png'
    hamburger_img_url = '/assets/hamburger-menu.svg'

    return html.Div(
        [
            #html.Img(
            #    src = hamburger_img_url,
            #    className='hamburger',
            #),
            html.Div(
                dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
                    <img
                        src='/assets/hamburger-menu-2.svg'
                        onclick='toggleSidebarVisible()'
                        class='clickable-icon icon'
                        title='Show or hide contents'
                    >
                '''),
                className='icon',
            ),
            html.Img(
                src = lightbulb_img_url,
                className='icon',
            ),
            html.H1(
                [
                    html.Span(
                        'EA Data',
                        className = 'data',
                    ),
                ],
                className='main-title short-title',
            ),
            html.H1(
                [
                    html.Span(
                        'Effective ',
                        className = 'effective',
                    ),
                    html.Span(
                        'Altruism ',
                        className = 'altruism',
                    ),
                    html.Span(
                        'Data',
                        className = 'data',
                    ),
                ],
                className = 'main-title long-title',
            ),
            html.Div(
                [
                    html.Div(
                        dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
                            <img
                                src="/assets/sun.svg"
                                onclick='toggleDarkMode()'
                                class='clickable-icon icon'
                                title="Change appearance"
                                id='darkmode-button'
                            >
                        '''),
                        className='icon',
                    ),
                    visdcc.Run_js(id='javascript-header'),
                    html.Div(
                        dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
                            <img
                                src='/assets/question-mark.svg'
                                onclick='toggleAboutVisibility()'
                                class='clickable-icon icon'
                                title='About'
                            >
                        '''),
                        className='icon',
                    ),
                ],
                className = 'right-icons',
            )

        ],
        className='header center',
        id="header-sidebar-visdcc"
    )
