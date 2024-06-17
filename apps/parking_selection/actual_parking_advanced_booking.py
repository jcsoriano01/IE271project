from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import pandas as pd
import json

from app import app
from apps import dbconnect as db
from datetime import datetime


layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3("Select Records")
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
                                                dbc.Input(type = 'text', id = 'psab_search_user_id', placeholder="Enter User ID")
                                                ,className='me-3'
                                            )
                                            ,dbc.Label("Last Name", width="auto")
                                            ,dbc.Col(
                                                dbc.Input(type = "text", id = 'psab_search_last_name',  placeholder="Last Name")
                                                ,className="me-3"
                                            )
                                            ,dbc.Label("Middle Name",  width="auto")
                                            ,dbc.Col(   
                                                dbc.Input(type = "text", id = 'psab_search_middle_name', placeholder="Middle Name")
                                                ,className="me-3"
                                            )
                                            ,dbc.Label("First Name", width="auto")
                                            ,dbc.Col(
                                                dbc.Input(type = "text", id = 'psab_search_first_name', placeholder="First Name")
                                                ,className="me-3"
                                            )
                                            ,dbc.Col(dbc.Button("Search",color="primary", n_clicks=0, id = 'psab_search_btn'),width="auto")
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
                            ,id = 'psab_user_record_search_result'
                        )
                    ]
                )

            ]
        )
    ]
)

@app.callback(
    [
        Output('psab_user_record_search_result','children')
    ],
    [
        Input('url','pathname')
        ,Input('psab_search_user_id', 'value')
        ,Input('psab_search_last_name', 'value')
        ,Input('psab_search_middle_name', 'value')
        ,Input('psab_search_first_name', 'value')
        #,Input('customers_search_btn', 'n_clicks')
    ]
)
def customers_loadlist(pathname, user_id, last_name, middle_name, first_name):
    if pathname == '/parking_selection/with_advanced_booking':
        sql = """
            SELECT
                d.adv_booking_applied_date,
                a.firstname,
                a.middlename,
                a.lastname,
                TO_CHAR(d.booking_date,'YYYY-MM-DD') AS booking_date,
                d.start_date,
                d.end_date,
                d.booking_id,
                e.floor,
                e.lot_no
            FROM users a
            JOIN registration b ON a.user_id = b.customer_id
            JOIN registration_status c ON b.registration_status_id = c.registration_status_id
            JOIN booking d ON d.registration_no = b.registration_no
            JOIN parking_slot e ON d.parking_id = e.parking_id
            WHERE is_active = true
            AND b.registration_status_id = 2
            AND d.is_adv_booking_apprv = 2
            AND TO_CHAR(d.booking_date,'YYYY-MM-DD') = TO_CHAR(CURRENT_TIMESTAMP,'YYYY-MM-DD')
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
            'adv_booking_applied_date', 'firstname', 'middlename', 'lastname', 'booking_date', 'start_date', 'end_date','booking_id','floor','lot_no'
        ]

        df = db.querydatafromdatabase(sql,values,cols)

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover = True, size = 'sm')
        return [table]
    else:
        raise PreventUpdate
 