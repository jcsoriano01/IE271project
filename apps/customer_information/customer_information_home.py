from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import base64

from urllib.parse import urlparse, parse_qs
from app import app
from apps import dbconnect as db
from datetime import datetime

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3("Search Customer Records")
                    ]
                )
                ,dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Form(
                                    dbc.Row(
                                        [
                                            dbc.Label('User ID', width = "auto")
                                            ,dbc.Col(
                                                dbc.Input(type = 'text', id = 'ci_search_user_id', placeholder="Enter User ID")
                                                ,className='me-3'
                                            )
                                            ,dbc.Label("Last Name", width="auto")
                                            ,dbc.Col(
                                                dbc.Input(type = "text", id = 'ci_search_last_name',  placeholder="Last Name")
                                                ,className="me-3"
                                            )
                                            ,dbc.Label("Middle Name",  width="auto")
                                            ,dbc.Col(   
                                                dbc.Input(type = "text", id = 'ci_search_middle_name', placeholder="Middle Name")
                                                ,className="me-3"
                                            )
                                            ,dbc.Label("First Name", width="auto")
                                            ,dbc.Col(
                                                dbc.Input(type = "text", id = 'ci_search_first_name', placeholder="First Name")
                                                ,className="me-3"
                                            )
                                            ,dbc.Col(dbc.Button("Search",color="primary", n_clicks=0, id = 'ci_search_btn'),width="auto")
                                        ]
                                        ,className= "g-2"
                                    )
                                )
                            ]
                        )
                        ,html.Hr()
                        ,html.Br()
                        ,html.Div(
                            "Result of Search will be shown here"
                            ,id = 'ci_user_record_search_result'
                        )
                    ]
                )

            ]
        )
    ]
    ,style={
                'backgroundColor': "#FFFFFF",
                'padding': '20px',
                'borderRadius': '5px',
                'minHeight': 'auto',
                'border': '1px solid #ced4da',
                'fontFamily': 'Georgia'
            }
)

@app.callback(
    [
        Output('ci_user_record_search_result','children')
    ],
    [
        Input('url','pathname')
        ,Input('ci_search_user_id', 'value')
        ,Input('ci_search_last_name', 'value')
        ,Input('ci_search_middle_name', 'value')
        ,Input('ci_search_first_name', 'value')
        #,Input('customers_search_btn', 'n_clicks')
    ]
)
def customers_loadlist(pathname, user_id, last_name, middle_name, first_name):
    if pathname == '/customer_information':
        sql = """
            SELECT
                a.created_date
                ,a.user_id
                ,a.firstname
                ,a.middlename
                ,a.lastname
                ,b.registration_no
                ,c.registration_status
            FROM users a
            JOIN registration b
            ON a.user_id = b.customer_id
            JOIN registration_status c
            ON b.registration_status_id = c.registration_status_id
            WHERE is_active = true
            """
        values = []
        

        if user_id:
            sql += " AND a.user_id = %s"
            values.append(f"{user_id}")
        if first_name:
            sql += " AND a.firstname ILIKE %s"
            values.append(f"%{first_name}%")
        if middle_name:
            sql += " AND a.middlename ILIKE %s"
            values.append(f"%{middle_name}%")
        if last_name:
            sql += " AND a.lastname ILIKE %s"
            values.append(f"%{last_name}%")

        cols = [
            'created_date', 'user_id', 'firstname', 'middlename','lastname','registration_no','registration_status'
        ]

        df = db.querydatafromdatabase(sql,values,cols)

        if df.shape:
            buttons = []
            for user_id in df['user_id']:
                buttons += [
                    html.Div(
                        dbc.Button(
                            'View'
                            ,href=f'/customer_information/view/view?mode=edit&id={user_id}'
                            ,size = 'sm'
                            ,color = 'info'
                            ,className="me-1"
                            ,style={'text-align':'center'}
                        )
                    )
                ]
            
            df['Action'] = buttons

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover = True, size = 'sm')
            return [table]
        else:
            return ["No records"]
    else:
        raise PreventUpdate