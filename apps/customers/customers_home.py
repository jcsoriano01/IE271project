from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db
from datetime import datetime

layout = html.Div(
    [
        dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardImg(src="/assets/new_customers_2.png"
                                                ,className = 'card-img d-block mx-auto w-50 py-5 h-25') #style={'display': 'block', 'margin': 'auto','width': '50%', 'height': 'auto','padding':'20px'}
                                    ,html.Hr()
                                    ,dbc.CardBody(
                                        [
                                            html.H4("Add New User", className="card-title", style={'center': True}),
                                            html.P(
                                                "Register new customers and their vehicles",
                                                className="card-text",
                                            ),
                                            dbc.Button("Register", color="primary", href = '/customer_registration/new'),
                                        ]
                                    ),
                                ]
                                #style={"width": "18rem"},
                            )
                        ]
                        ,width = 4
                    )
                    ,dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardImg(src="/assets/customers_edit.png",className = 'card-img d-block mx-auto w-50 py-5 h-25')
                                    ,html.Hr()
                                    ,dbc.CardBody(
                                        [
                                            html.H4("Edit User Information", className="card-title", style={'center': True}),
                                            html.P(
                                                "Modify or update your information",
                                                className="card-text",
                                            ),
                                            dbc.Button("Edit", color="primary", href = "/customer_registration/edit"),
                                        ]
                                    ),
                                ]
                                #style={"width": "18rem"},
                            )
                        ]
                        ,width = 4
                    )
                    ,dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardImg(src="/assets/customers_approval.png", className = 'card-img d-block mx-auto w-50 py-5 h-25')
                                        ,html.Hr()
                                        ,dbc.CardBody(
                                            [
                                                html.H4("Approve Registration", className="card-title", style={'center': True}),
                                                html.P(
                                                    "Modify or update your information",
                                                    className="card-text",
                                                ),
                                                dbc.Button("Approve", color="primary"),
                                            ]
                                        ),
                                    ]
                                    #style={"width": "18rem"},
                                )
                            ]
                            ,width = 4
                        )
                ]
            )
    ]
    ,style={'font-family':'Georgia','color':'#696969'}
)

#devicy . 