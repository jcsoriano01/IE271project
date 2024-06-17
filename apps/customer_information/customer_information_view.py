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
        dcc.Store(id='selected_parking_lot', storage_type='memory', data = 0),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                html.Img(id='ci_customer_image_result',
                                style={'display': 'block', 'margin': 'auto', 'width': '50%', 'height': 'auto'})
                            ),
                            html.Br(),
                            html.H5(
                                id='ci_customer_name',
                                style={
                                    'textAlign': 'center',
                                    'margin': '0'
                                }
                            ),
                            html.Hr(),
                            html.P(
                                id='ci_customer_created_date',
                                style={
                                    'textAlign': 'left',
                                    'color':'#696969'
                                }
                            ),
                            html.P(
                                id='ci_customer_approval_date',
                                style={
                                    'textAlign': 'left',
                                    'color':'#696969'
                                }
                            ),
                            html.P(
                                id='ci_customer_car_brand',
                                style={
                                    'textAlign': 'left',
                                    'color':'#696969'
                                }
                            ),
                            html.P(
                                id='ci_customer_car_model',
                                style={
                                    'textAlign': 'left',
                                    'color':'#696969'
                                }
                            ),
                            html.P(
                                id='ci_customer_plate_number',
                                style={
                                    'textAlign': 'left',
                                    'color':'#696969'
                                }
                            )
                        ]
                    ),
                    style={
                            'backgroundColor': "#FFFFFF",
                            'padding': '20px',
                            'borderRadius': '5px',
                            'minHeight': 'auto',
                            'border': '1px solid #ced4da',
                            'fontFamily': 'Georgia'
                        }
                    ,width=3
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        [html.H5("YTD Total Booking", style={'margin': 0})],
                                                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px','background-color':'primary','fontFamily': 'Georgia'}
                                                    ),
                                                    dbc.CardBody(
                                                        [
                                                            html.Div(
                                                                "0",
                                                                id='ci_ytd_total_booking',
                                                                style={
                                                                    'display': 'flex', 
                                                                    'align-items': 'center', 
                                                                    'justify-content': 'center', 
                                                                    'color': "slategrey",
                                                                    'font-size': '20px',  # Adjust the font size as needed
                                                                    'font-weight': 'bold'  # Make the text bold
                                                                },
                                                                className='card-title',
                                                            )
                                                        ]
                                                    )
                                                ],
                                                style={"width": "18rem"},
                                            )
                                        ]
                                        ,width= "auto"
                                    ),
                            dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        [html.H5("Average Booking Per Month", style={'margin': 0})],
                                                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px','background-color':'primary','fontFamily': 'Georgia'}
                                                    ),
                                                    dbc.CardBody(
                                                        [
                                                            html.Div(
                                                                "0",
                                                                id='ci_avg_booking_month',
                                                                style={
                                                                    'display': 'flex', 
                                                                    'align-items': 'center', 
                                                                    'justify-content': 'center', 
                                                                    'color': "slategrey",
                                                                    'font-size': '20px',  # Adjust the font size as needed
                                                                    'font-weight': 'bold'  # Make the text bold
                                                                },
                                                                className='card-title',
                                                            )
                                                        ]
                                                    )
                                                ],
                                                style={"width": "18rem"},
                                            )
                                        ]
                                        ,width= "auto"
                                    ),
                            dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        [html.H5("Average Parking Duration", style={'margin': 0})],
                                                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px','background-color':'primary','fontFamily': 'Georgia'}
                                                    ),
                                                    dbc.CardBody(
                                                        [
                                                            html.Div(
                                                                "0",
                                                                id='ci_avg_parking_duration',
                                                                style={
                                                                    'display': 'flex', 
                                                                    'align-items': 'center', 
                                                                    'justify-content': 'center', 
                                                                    'color': "slategrey",
                                                                    'font-size': '20px',  # Adjust the font size as needed
                                                                    'font-weight': 'bold'  # Make the text bold
                                                                },
                                                                className='card-title',
                                                            )
                                                        ]
                                                    )
                                                ],
                                                style={"width": "18rem"},
                                            )
                                        ]
                                        ,width= "auto"
                                    ),
                            ]  
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    html.H5("Parking History", style={'margin': 0})
                                                ),
                                                dbc.CardBody(
                                                    [
                                                        html.Div(
                                                            "Parking transactions will be shown here"
                                                            ,id = 'ci_parking_transactions'
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ],
                        )
                    ]
                    ,width = 9
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
        Output('ci_customer_image_result', 'src'),
        Output('ci_customer_name', 'children'),
        Output('ci_customer_created_date', 'children'),
        Output('ci_customer_approval_date', 'children'),
        Output('ci_customer_car_brand', 'children'),
        Output('ci_customer_car_model', 'children'),
        Output('ci_customer_plate_number', 'children'),
        Output('ci_ytd_total_booking', 'children'),
        Output('ci_avg_booking_month', 'children'),
        Output('ci_avg_parking_duration', 'children')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def customer_information_customerprofile_load(pathname, search):
    if pathname == '/customer_information/view/view':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        to_load = 1 if create_mode == 'edit' else 0

        if to_load == 1:
            user_id = parse_qs(parsed.query).get('id', [None])[0]

            if not user_id:
                raise PreventUpdate

            sql = """
                SELECT
                    COALESCE(firstname, '') || ' ' || COALESCE(lastname, '')  AS name_,
                    image,
                    created_date,
                    approval_date,
                    car_brand,
                    car_model,
                    plate_number
                FROM users a
                JOIN registration b
                ON a.user_id = b.customer_id
                WHERE user_id = %s
            """
            values = [user_id]
            col = ['name_', 'image','created_date','approval_date','car_brand','car_model','plate_number']

            df = db.querydatafromdatabase(sql, values, col)

            if df.empty:
                raise PreventUpdate

            # Extract values from the DataFrame
            name = df['name_'][0]
            image_data = df['image'][0]
            created_date = df['created_date'][0]
            approval_date = df['approval_date'][0]
            car_brand = df['car_brand'][0]
            car_model = df['car_model'][0]
            plate_number = df['plate_number'][0]

            image = f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}" if image_data else None

            sql2 = """
            SELECT
                TO_CHAR(booking_date,'YYYY') AS year
                ,customer_id
                ,COUNT(DISTINCT booking_id) AS booking_count
            FROM booking
            LEFT JOIN registration
            ON booking.registration_no = registration.registration_no
            WHERE customer_id = %s
            AND TO_CHAR(booking_date,'YYYY') = TO_CHAR(CURRENT_TIMESTAMP,'YYYY')
            GROUP BY
                TO_CHAR(booking_date,'YYYY')
                ,customer_id
            """

            values_2 = [user_id]
            cols2 = ['booking_year','customer_id','booking_count']
            result2 = db.querydatafromdatabase(sql2,values_2,cols2)
            if result2.empty:
                ytd_count = 0
            else:
                ytd_count = result2['booking_count'].iloc[0]

            print(f'Result ytd:{ytd_count}')
             #if pd.notna(result2['booking_count'].iloc[0]) else 1
            
            sql3 = """
            SELECT
                TO_CHAR(booking_date,'YYYY') AS year
                ,customer_id
                ,COUNT(DISTINCT booking_id) AS booking_count
                ,COUNT(DISTINCT TO_CHAR(booking_date,'YYYY-MM')) AS booking_month
                ,COUNT(DISTINCT booking_id)/COUNT(DISTINCT TO_CHAR(booking_date,'YYYY-MM')) AS avg_booking_month
            FROM booking
            LEFT JOIN registration
            ON booking.registration_no = registration.registration_no
            WHERE customer_id = %s
            AND TO_CHAR(booking_date,'YYYY') = TO_CHAR(CURRENT_TIMESTAMP,'YYYY')
            GROUP BY
                TO_CHAR(booking_date,'YYYY')
                ,customer_id 
            """
            values_3 = [user_id]
            cols3 = ['booking_year','customer_id','booking_count','booking_month','avg_booking_month']
            result3 = db.querydatafromdatabase(sql3,values_3,cols3)
            if result3.empty:
                mtd_count = 0
            else:
                mtd_count = result3['avg_booking_month'].iloc[0]
                #mtd_count = str(mtd_count)
            print(f'Result mtd:{mtd_count}')

            sql4 = """
            SELECT
                TO_CHAR(booking_date,'YYYY') AS year
                ,customer_id
                ,SUM(end_date::TIME - start_date::TIME)AS book_hours
                ,COUNT(DISTINCT booking_id) AS booking_count
                ,EXTRACT(HOUR FROM SUM(end_date::TIME - start_date::TIME)/COUNT(DISTINCT booking_id)) AS avg_booking_hours
                ,EXTRACT(MINUTE FROM SUM(end_date::TIME - start_date::TIME)/COUNT(DISTINCT booking_id)) AS avg_booking_minutes
            FROM booking
            LEFT JOIN registration
            ON booking.registration_no = registration.registration_no
            WHERE customer_id = %s
            AND TO_CHAR(booking_date,'YYYY') = TO_CHAR(CURRENT_TIMESTAMP,'YYYY')
            GROUP BY
                TO_CHAR(booking_date,'YYYY')
                ,customer_id 
            """
            values_4 = [user_id]
            cols4 = ['booking_year','customer_id','book_hours','booking_count','avg_booking_hours','avg_booking_minutes']
            result4 = db.querydatafromdatabase(sql4,values_4,cols4)
            if result4.empty:
                avg_booking_hours = 0
                avg_booking_minutes = 0
            else:
                avg_booking_hours = result4['avg_booking_hours'].iloc[0]
                avg_booking_minutes = result4['avg_booking_minutes'].iloc[0]
            

            return image, name, f"Registration Date: {created_date}", f"Approval Date: {approval_date}", f"Car Brand: {car_brand}", f"Car Model: {car_model}", f"Plate No.: {plate_number}", f"{ytd_count}",  f"{mtd_count}", f"{int(avg_booking_hours):02d}:{int(avg_booking_minutes):02d}"
            #return name, f"Registered Date: {created_date}"
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('ci_parking_transactions','children')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url', 'search')
    ]
)
def customer_information_parking_history(pathname, search):
    if pathname == '/customer_information/view/view':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        to_load = 1 if create_mode == 'edit' else 0

        if to_load == 1:
            user_id = parse_qs(parsed.query).get('id', [None])[0]

            if not user_id:
                raise PreventUpdate
            
            sql = """
                SELECT
                    booking_date
                    ,start_date AS time_start
                    ,end_date AS time_end
                    ,is_advanced_booking
                    ,is_adv_booking_apprv AS is_approved
                    ,floor
                    ,lot_no
                FROM booking
                LEFT JOIN registration
                ON booking.registration_no = registration.registration_no
                LEFT JOIN users
                ON users.user_id = registration.customer_id
                LEFT JOIN parking_slot
                ON parking_slot.parking_id = booking.parking_id
                WHERE users.user_id = %s
                ORDER BY booking_date DESC
            """
            values = [user_id]
            cols = ['booking_date', 'time_start', 'time_end' ,'is_advanced_booking', 'is_approved', 'floor', 'lot_no']
            result = db.querydatafromdatabase(sql,values, cols)
            booking_date = result['booking_date'].iloc[0]
            time_start = result['time_start'].iloc[0]
            time_end = result['time_end'].iloc[0]
            is_advanced_booking = result['is_advanced_booking'].iloc[0]
            is_approved = result['is_approved'].iloc[0]
            floor = result['floor'].iloc[0]
            lot_no = result['lot_no'].iloc[0]
            table = dbc.Table.from_dataframe(result, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return ["No records"]
    else:
        raise PreventUpdate