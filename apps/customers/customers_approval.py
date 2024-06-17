from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db
from datetime import datetime

layout = html.Div(
    [
        dcc.Store(id = 'approval-trigger', data=0)
        ,dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Success")),
                dbc.ModalBody("The selected record has been successfully approved."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                ),
            ],
            id="modal",
            is_open=False,
        )
        ,dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Rejected")),
                dbc.ModalBody("The selected record has been rejected."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="reject_close", className="ms-auto", n_clicks=0)
                ),
            ],
            id="reject_modal",
            is_open=False,
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [html.H5("For Approval Count", style={'margin': 0})],
                                    style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px', 'background-color':'yellowgreen'}
                                ),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            "The number of for approval will be shown here",
                                            id='for_approval_count',
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
                                            id='for_approval_sla',
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
                                                                dbc.Input(type='text', id='customers_search_user_id', placeholder="Enter User ID"),
                                                                className='me-3'
                                                            ),
                                                            dbc.Col(
                                                                dbc.Input(type="text", id='customers_search_last_name', placeholder="Enter Last Name"),
                                                                className="me-3"
                                                            ),
                                                            dbc.Col(
                                                                dbc.Input(type="text", id='customers_search_middle_name', placeholder="Enter Middle Name"),
                                                                className="me-3"
                                                            ),
                                                            dbc.Col(
                                                                dbc.Input(type="text", id='customers_search_first_name', placeholder="Enter First Name"),
                                                                className="me-3"
                                                            ),
                                                            dbc.Col(dbc.Button("Search", color="primary", n_clicks=0, id='customers_search_btn'), width="auto")
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
                                            id='user_record_approval'
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
    Output('for_approval_count','children'),
    [
        Input('url','pathname'),
        Input('approval-trigger','data'),
    ]
)
def customers_for_approval_count(pathname,trigger_value):
    if pathname == '/customer_registration/for_approval':
        sql = """
        SELECT
            COUNT(DISTINCT user_id) AS count_approval
        FROM users a
        JOIN registration b ON a.user_id = b.customer_id
        JOIN registration_status c ON b.registration_status_id = c.registration_status_id
        WHERE is_active = true
        AND b.registration_status_id = 1
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
    Output('for_approval_sla','children'),
    [
        Input('url','pathname'),
        Input('approval-trigger','data'),
    ]
)
def customers_approval_sla(pathname,trigger_value):
    if pathname == '/customer_registration/for_approval':
        sql = """
        SELECT 
            ROUND(COUNT(DISTINCT CASE WHEN EXTRACT(DAYS FROM (COALESCE(NOW(),approval_date) - created_date)) <= 2 THEN registration_no END)::DECIMAL/(COUNT(DISTINCT registration_no)::DECIMAL) * 100,2) AS sla
        FROM users a
        JOIN registration b ON a.user_id = b.customer_id
        WHERE is_active = true
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
    Output('user_record_approval', 'children'),
    [
        Input('url', 'pathname'),
        Input('customers_search_btn', 'n_clicks'),
        Input('approval-trigger','data'),
    ],
    [
        State('customers_search_user_id', 'value'),
        State('customers_search_last_name', 'value'),
        State('customers_search_middle_name', 'value'),
        State('customers_search_first_name', 'value')
    ]
)
def customers_loadlist(pathname, n_clicks, trigger_value, user_id, last_name, middle_name, first_name):
    if pathname == '/customer_registration/for_approval':
        sql = """
            SELECT
                a.created_date,
                a.firstname,
                a.middlename,
                a.lastname,
                b.registration_no,
                EXTRACT(DAY FROM NOW() - created_date) AS age,
                a.user_id
            FROM users a
            JOIN registration b ON a.user_id = b.customer_id
            JOIN registration_status c ON b.registration_status_id = c.registration_status_id
            WHERE is_active = true
            AND b.registration_status_id = 1
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
            'created_date', 'firstname', 'middlename', 'lastname', 'registration_no', 'created_date', 'user_id'
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for idx, user_id in enumerate(df['user_id']):
                buttons.append(
                    dbc.Button(
                        'Approve',
                        id={'type': 'approve_button', 'index': user_id},
                        size='sm',
                        color='info',
                        className='me-1',
                        style={'text-align': 'center'}
                    )
                )
            df['Action'] = buttons

            buttons2 = []
            for idx, user_id in enumerate(df['user_id']):
                buttons2.append(
                    dbc.Button(
                        'Reject',
                        id={'type': 'reject_button', 'index': user_id},
                        size='sm',
                        color='info',
                        className='me-1',
                        style={'text-align': 'center'}
                    )
                )
            df['Action2'] = buttons2

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return ["No records"]
    else:
        raise PreventUpdate

# @app.callback(
#     Output('modal', 'is_open'),
#     Output('approval-trigger','data'),
#     [Input({'type': 'approve_button', 'index': ALL}, 'n_clicks')
#      #Input({'type': 'reject_button', 'index': ALL}, 'n_clicks')
#      ,Input("close","n_clicks")
#      ],

#     [State('modal', 'is_open')
#     ,State('approval-trigger','data') 
#     ],
#     prevent_initial_call=True,
# )
# def update_registration_status(n_clicks, close_click, is_open, trigger_value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         raise PreventUpdate
#     else:
#         button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#         if button_id == 'close':
#             return not is_open, trigger_value
#         else:
#             user_id_to_approve = eval(button_id)['index']

#             if n_clicks and all(clicks is None for clicks in n_clicks):
#                 raise PreventUpdate
            
#             current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#             sql_update = """
#                 UPDATE registration
#                 SET registration_status_id = 3
#                     ,approval_date = %s
#                 WHERE customer_id = %s
#             """
#             db.modifydatabase(sql_update, [current_timestamp,user_id_to_approve])

#             return True, trigger_value + 1
            
@app.callback(
    [
        Output('modal', 'is_open'),
        Output('approval-trigger', 'data'),
        Output('reject_modal', 'is_open'),
    ],
    [
        Input({'type': 'approve_button', 'index': ALL}, 'n_clicks'),
        Input({'type': 'reject_button', 'index': ALL}, 'n_clicks'),
        Input("close", "n_clicks"),
        Input('reject_close', 'n_clicks'),
    ],
    [
        State('modal', 'is_open'),
        State('approval-trigger', 'data'),
        State('reject_modal','is_open'),
        #State('reject-trigger', 'data')
    ],
    prevent_initial_call=True,
)
def update_registration_status(approve_clicks, reject_clicks, close_click, rekect_close_click,is_open, approval_trigger, reject_is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'close':
            return not is_open, approval_trigger, not reject_is_open

        if 'approve_button' in button_id:
            user_id = eval(button_id)['index']
            if approve_clicks and all(click is None for click in approve_clicks):
                raise PreventUpdate
            
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            sql_update = """
                UPDATE registration
                SET registration_status_id = 2,
                    approval_date = %s
                WHERE customer_id = %s
            """
            db.modifydatabase(sql_update, [current_timestamp, user_id])
            return True, approval_trigger + 1, False

        elif 'reject_button' in button_id:
            user_id = eval(button_id)['index']
            if reject_clicks and all(click is None for click in reject_clicks):
                raise PreventUpdate
            
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            sql_update = """
                UPDATE registration
                SET registration_status_id = 3,
                    rejection_date = %s
                WHERE customer_id = %s
            """
            db.modifydatabase(sql_update, [current_timestamp, user_id])
            return False, approval_trigger + 1, True

        raise PreventUpdate
