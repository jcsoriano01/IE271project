from dash import dcc
from dash import html, callback_context
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL
from urllib.parse import urlparse, parse_qs

from app import app
from apps import dbconnect as db
from datetime import datetime
import hashlib

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    #html.H2('EZPark', className='text-center'),
                    html.Div(
                        html.H2('EZPark', className='text-center', style={'color': 'white'}),
                        style={'backgroundColor': 'darkslategrey', 'padding': '10px'}
                    ),
                    html.Br(),
                    dbc.Alert("Username or Password is incorrect", color='danger', id='login_alert', is_open=False),
                    dbc.Row(
                        [
                            dbc.Label("Username", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type='text', id='login_username'
                                ),
                                width=6,
                            )
                        ],
                        className='mb-3 justify-content-center'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Password", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type='password', id='login_password'
                                ),
                                width=6
                            )
                        ],
                        className='mb-3 justify-content-center'
                    ),
                    html.Br(),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Button('Login', color='secondary', id='login_loginbtn'),
                                    #width='auto',
                                    #className='text-center'
                                ]
                                ,width = 1  
                                ,className='text-center'
                            ),
                            dbc.Col(
                                [
                                    #html.A('Signup', href='/customer_registration/new'),
                                    dbc.Button('Signup', color='link', href='/signup'),
                                    #className='text-center'
                                ]
                                ,width = 3
                                ,className='text-center'
                            ), 
                        ]
                        ,className='justify-content-start'
                        
                    ),
                ],
                width=9,
                className='align-self-center'
            ),
            className='justify-content-center col-9'
        ),
    ],
    className='vh-100 d-flex align-items-center justify-content-center col-12'
)

@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
    ],
    [
        Input('login_loginbtn', 'n_clicks'),
        Input('sessionlogout', 'modified_timestamp'),
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
        State('url', 'pathname'),
    ]
)
def loginprocess(loginbtn, sessionlogout_time, username, password, sessionlogout, currentuserid, pathname):
    ctx = callback_context

    if ctx.triggered:
        openalert = False
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate

    if eventid == 'login_loginbtn':
        if loginbtn and username and password:
            sql = """
            SELECT a.user_id
            FROM employees a
            LEFT JOIN users b
            ON a.user_id = b.user_id
            WHERE user_name = %s
            AND user_password = %s
            AND is_active = True
            """

            # we match the encrypted input to the encrypted password in the db
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()

            values = [username, password]
            cols = ['userid']
            df = db.querydatafromdatabase(sql, values, cols)

            if df.shape[0]:
                currentuserid = df['userid'][0]
            else:
                currentuserid = -1
                openalert = True

        elif eventid == 'sessionlogout' and pathname == '/logout':
            currentuserid = -1

        else:
            raise PreventUpdate

        return [openalert, currentuserid]

@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'),
    ]
)
def routelogin(logintime, userid):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0:
            url = '/home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]


