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
        dcc.Store(id = 'adv_booking_approval-trigger', data=0)
        ,dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Success")),
                dbc.ModalBody("The selected record has been successfully approved."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                ),
            ],
            id="adv_booking_modal",
            is_open=False,
        )
        ,dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Rejected")),
                dbc.ModalBody("The selected record has been successfully rejected."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="adv_booking_rejected_close", className="ms-auto", n_clicks=0)
                ),
            ],
            id="adv_booking_reject_modal",
            is_open=False,
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [html.H5("For Approval", style={'margin': 0})],
                                    style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px', 'background-color':'yellowgreen'}
                                ),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            "The number of for approval will be shown here",
                                            id='adv_booking_for_approval_count',
                                            style={
                                                'display': 'flex', 
                                                'align-items': 'center', 
                                                'justify-content': 'center', 
                                                'color': "slategrey",
                                                'font-size': '48px',  # Adjust the font size as needed
                                                'font-weight': 'bold'  # Make the text bold
                                            },
                                            className='card-title',
                                        )
                                    ]
                                )
                            ],
                            style={"width": "18rem"},
                        ),
                        html.Br(),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [html.H5("Service Level", style={'margin': 0})],
                                    style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px','background-color':'teal','color':'white'}
                                ),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            "Service Level Agreement",
                                            id='adv_booking_for_approval_sla',
                                            style={
                                                'display': 'flex', 
                                                'align-items': 'center', 
                                                'justify-content': 'center', 
                                                'color': "slategrey",
                                                'font-size': '48px',  # Adjust the font size as needed
                                                'font-weight': 'bold'  # Make the text bold
                                            },
                                            className='card-title',
                                        )
                                    ]
                                )
                            ],
                            style={"width": "18rem"},
                        )
                    ],
                    width=3
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [html.H5("For Approval Records", style={'margin': 0})],
                                    style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px'}
                                ),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                dbc.Form(
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dbc.Input(type='text', id='adv_booking_search_user_id', placeholder="Enter User ID"),
                                                                className='me-3'
                                                            ),
                                                            dbc.Col(
                                                                dbc.Input(type="text", id='adv_booking_search_last_name', placeholder="Enter Last Name"),
                                                                className="me-3"
                                                            ),
                                                            dbc.Col(
                                                                dbc.Input(type="text", id='adv_booking_search_middle_name', placeholder="Enter Middle Name"),
                                                                className="me-3"
                                                            ),
                                                            dbc.Col(
                                                                dbc.Input(type="text", id='adv_booking_search_first_name', placeholder="Enter First Name"),
                                                                className="me-3"
                                                            ),
                                                            dbc.Col(dbc.Button("Search", color="primary", n_clicks=0, id='adv_booking_search_btn'), width="auto")
                                                        ],
                                                        className="g-2"
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Hr(),
                                        html.Br(),
                                        html.Div(
                                            "Result of Search will be shown here",
                                            id='adv_booking_user_record_approval'
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output('adv_booking_for_approval_count','children'),
    [
        Input('url','pathname'),
        Input('adv_booking_approval-trigger','data'),
    ]
)
def customers_for_approval_count(pathname,trigger_value):
    if pathname == '/advanced_booking/for_approval':
        sql = """
        SELECT
        COUNT(DISTINCT booking_id) AS count_approval
        FROM users a
        JOIN registration b ON a.user_id = b.customer_id
        JOIN registration_status c ON b.registration_status_id = c.registration_status_id
        JOIN booking d ON b.registration_no = d.registration_no
        WHERE is_active = true
        AND b.registration_status_id = 2
        AND d.is_advanced_booking is True
        AND d.is_adv_booking_apprv = 1
        """ 
        values = []

        cols = ['count_approval']
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0] >0:
            count = df.iloc[0]['count_approval']
            return str(count)
        else:
            return "0"
    else:
        return "0"


@app.callback(
    Output('adv_booking_for_approval_sla','children'),
    [
        Input('url','pathname'),
        Input('adv_booking_approval-trigger','data'),
    ]
)
def customers_approval_sla(pathname,trigger_value):
    if pathname == '/advanced_booking/for_approval':

        sql = """
        SELECT 
            ROUND(COUNT(DISTINCT CASE WHEN EXTRACT(DAYS FROM (COALESCE(NOW(),adv_booking_approved_date) - adv_booking_applied_date)) <= 2 AND is_advanced_booking is True THEN booking_id END)::DECIMAL/COUNT(DISTINCT CASE WHEN is_advanced_booking is True THEN booking_id END)::DECIMAL * 100,2) AS sla
        FROM booking
        """
        values = []

        cols = ['sla']
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0] >0:
            count = df.iloc[0]['sla']
            return str(count)+"%"
        else:
            return "0%"
    else:
        return "0%"


@app.callback(
    Output('adv_booking_user_record_approval', 'children'),
    [
        Input('url', 'pathname'),
        Input('adv_booking_search_btn', 'n_clicks'),
        Input('adv_booking_approval-trigger','data'),
    ],
    [
        State('adv_booking_search_user_id', 'value'),
        State('adv_booking_search_last_name', 'value'),
        State('adv_booking_search_middle_name', 'value'),
        State('adv_booking_search_first_name', 'value')
    ]
)
def customers_loadlist(pathname, n_clicks, trigger_value, user_id, last_name, middle_name, first_name):
    if pathname == '/advanced_booking/for_approval':
        sql = """
            SELECT
                d.adv_booking_applied_date,
                a.firstname,
                a.middlename,
                a.lastname,
                EXTRACT(DAY FROM NOW() - adv_booking_applied_date) AS age,
                TO_CHAR(d.booking_date,'YYYY-MM-DD') AS booking_date,
                d.start_date,
                d.end_date,
                d.parking_id,
                d.booking_id
            FROM users a
            JOIN registration b ON a.user_id = b.customer_id
            JOIN registration_status c ON b.registration_status_id = c.registration_status_id
            JOIN booking d ON d.registration_no = b.registration_no
            WHERE is_active = true
            AND b.registration_status_id = 2
            AND d.is_adv_booking_apprv = 1
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
            'adv_booking_applied_date', 'firstname', 'middlename', 'lastname', 'age', 'booking_date', 'start_date','end_date','parking_id', 'booking_id'
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for idx, booking_id in enumerate(df['booking_id']):
                buttons.append(
                    dbc.Button(
                        'Approve',
                        id={'type': 'adv_booking_approve_button', 'index': booking_id},
                        size='sm',
                        color='info',
                        className='me-1',
                        style={'text-align': 'center'}
                    )
                )
            df['Action'] = buttons

            buttons2 = []
            for idx, booking_id in enumerate(df['booking_id']):
                buttons2.append(
                    dbc.Button(
                        'Reject',
                        id={'type': 'adv_booking_reject_button', 'index': booking_id},
                        size='sm',
                        color='secondary',
                        className='me-1',
                        style={'text-align': 'center'}
                    )
                )
            df['Action2'] = buttons2

            df = df.drop(['adv_booking_applied_date'], axis=1)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return ["No records"]
    else:
        raise PreventUpdate


@app.callback(
    Output('adv_booking_modal', 'is_open'),
    Output('adv_booking_approval-trigger', 'data'),
    Output('adv_booking_reject_modal', 'is_open'),
    [Input({'type': 'adv_booking_approve_button', 'index': ALL}, 'n_clicks'),
     Input({'type': 'adv_booking_reject_button', 'index': ALL},'n_clicks'),
     Input("close", "n_clicks"),
     Input("adv_booking_rejected_close", "n_clicks"),
     ],
    [State('adv_booking_modal', 'is_open'),
     State('adv_booking_approval-trigger', 'data'),
     State('adv_booking_reject_modal','is_open') ,
    ],
    prevent_initial_call=True,
)
def update_registration_status(n_clicks_list, reject_clicks, close_click, reject_close_click,is_open, trigger_value,reject_is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if triggered_id == 'close':
            return not is_open, trigger_value, reject_is_open
        elif triggered_id == 'adv_booking_rejected_close':
            return is_open, trigger_value, not reject_is_open
        elif 'adv_booking_approve_button' in triggered_id:
            # Get the button index (booking_id)
            triggered_button = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
            if 'index' in triggered_button:
                booking_id_to_approve = triggered_button['index']
            else:
                raise PreventUpdate

            # Check if the button has been clicked
            if all(clicks is None for clicks in n_clicks_list) or all(clicks == 0 for clicks in n_clicks_list):
                raise PreventUpdate

            # Update the registration_status_id in the database
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql_update = """
                UPDATE booking
                SET is_adv_booking_apprv = 2,
                    adv_booking_approved_date = %s
                WHERE booking_id = %s
            """
            db.modifydatabase(sql_update, [current_timestamp, booking_id_to_approve])

            return True, trigger_value + 1, False
        elif 'adv_booking_reject_button' in triggered_id:
            triggered_button = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
            if 'index' in triggered_button:
                booking_id_to_approve = triggered_button['index']
            else:
                raise PreventUpdate

            # Check if the button has been clicked
            if all(clicks is None for clicks in reject_clicks) or all(clicks == 0 for clicks in reject_clicks):
                raise PreventUpdate

            # Update the registration_status_id in the database
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql_update = """
                UPDATE booking
                SET is_adv_booking_apprv = 3,
                    adv_booking_rejected_date = %s
                WHERE booking_id = %s
            """
            db.modifydatabase(sql_update, [current_timestamp, booking_id_to_approve])

            return False, trigger_value + 1, True