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
        dcc.Store(id='ps_selected_parking_lot', storage_type='memory', data = 0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Success")),
                dbc.ModalBody("The selected record has been successfully approved."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                ),
            ],
            id="ps_booking_modal",
            is_open=False,
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                html.Img(id='ps_customer_image_result',
                                style={'display': 'block', 'margin': 'auto', 'width': '50%', 'height': 'auto'})
                            ),
                            html.Br(),
                            html.H5(
                                id='ps_customer_name',
                                style={
                                    'textAlign': 'center',
                                    'margin': '0'
                                }
                            ),
                            html.Hr(),
                            html.P(
                                id='ps_customer_created_date',
                                style={
                                    'textAlign': 'left',
                                    'color':'#696969'
                                }
                            ),
                            html.P(
                                id='ps_customer_approval_date',
                                style={
                                    'textAlign': 'left',
                                    'color':'#696969'
                                }
                            ),
                            html.P(
                                id='ps_customer_car_brand',
                                style={
                                    'textAlign': 'left',
                                    'color':'#696969'
                                }
                            ),
                            html.P(
                                id='ps_customer_car_model',
                                style={
                                    'textAlign': 'left',
                                    'color':'#696969'
                                }
                            ),
                            html.P(
                                id='ps_customer_plate_number',
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
                                                        [html.H5("YTD Advanced Booking", style={'margin': 0})],
                                                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px','background-color':'primary','fontFamily': 'Georgia'}
                                                    ),
                                                    dbc.CardBody(
                                                        [
                                                            html.Div(
                                                                "0",
                                                                id='ps_ytd_advanced_booking',
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
                                                        [html.H5("MTD Advanced Booking", style={'margin': 0})],
                                                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px','background-color':'primary','fontFamily': 'Georgia'}
                                                    ),
                                                    dbc.CardBody(
                                                        [
                                                            html.Div(
                                                                "0",
                                                                id='ps_mtd_advanced_booking',
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
                                                        [html.H5("MTD Booked Parking", style={'margin': 0})],
                                                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px','background-color':'primary','fontFamily': 'Georgia'}
                                                    ),
                                                    dbc.CardBody(
                                                        [
                                                            html.Div(
                                                                "0",
                                                                id='ps_booked_parking',
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
                                                    html.H5("Booking Information", style={'margin': 0})
                                                ),
                                                dbc.CardBody(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Label("Parking Date: "),
                                                                        dcc.DatePickerSingle(
                                                                            id='ps_date_picker',
                                                                            date=datetime.now().strftime('%Y-%m-%d'),
                                                                            min_date_allowed = datetime.now().strftime('%Y-%m-%d'),
                                                                            max_date_allowed = datetime.now().strftime('%Y-%m-%d'),
                                                                            display_format='YYYY-MM-DD',
                                                                            style={'width': '100%'}
                                                                        ),
                                                                        dbc.Label("Parking Start Time: "),
                                                                        #dcc.Dropdown(
                                                                        #    id='ps_time_picker_start',
                                                                            #options=[{'label': f"{i:02d}:00", 'value': f"{i:02d}:00"} for i in range(24)],
                                                                            #value='00:00',
                                                                            #value = datetime.now().strftime('%H:%M'),
                                                                            #style={'width': '100%'}
                                                                        #)
                                                                        dcc.Input(
                                                                            id='ps_time_picker_start',
                                                                            type='time',
                                                                            value=datetime.now().strftime('%H:%M'),
                                                                            style={'width': '100%'}
                                                                        ),
                                                                    ],
                                                                    width=3
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Label("Floor:"),
                                                                        dcc.Dropdown(
                                                                            id='ps_floor',
                                                                            options=[
                                                                                {'label': 'Level 1', 'value': 1},
                                                                                {'label': 'Level 2', 'value': 2},
                                                                                {'label': 'Level 3', 'value': 3}
                                                                            ],
                                                                            #value='Level 1',
                                                                            style={'width': '100%'}
                                                                        ),
                                                                        dbc.Label("Parking End Time: "),
                                                                        dcc.Dropdown(
                                                                            id='ps_time_picker_end',
                                                                            options=[{'label': f"{i:02d}:00", 'value': f"{i:02d}:00"} for i in range(24)],
                                                                            value='00:00',
                                                                            style={'width': '100%'}
                                                                        )
                                                                    ],
                                                                    width=3
                                                                )
                                                                ,dbc.Col(
                                                                    [
                                                                        dbc.Label("Available Lots:"),
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    dbc.Button(
                                                                                        f"Lot {i*3 + j + 1}",
                                                                                        id=f"ps_parking_lot_{i*3 + j + 1}",
                                                                                        #color="info",
                                                                                        style={'margin': '5px', 'width':'75px'}
                                                                                    ),
                                                                                    width=4
                                                                                ) for i in range(5) for j in range(3)
                                                                            ]
                                                                        )
                                                                    ]
                                                                    ,width = 6
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                                ,dbc.CardFooter(
                                                    dbc.Button(
                                                        'Submit'
                                                        ,id = 'ps_submit'
                                                        ,n_clicks=0
                                                    )
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
    ],
    style={'backgroundColor': '#FFFFF0'}
)


@app.callback(
    [
        Output('ps_selected_parking_lot','data')
    ],
    [
        Input(f'ps_parking_lot_{i * 3 + j + 1}', 'n_clicks') for i in range(5) for j in range(3)
    ],
    [
        Input('ps_submit','n_clicks')
    ]
)
def update_selected_parking_lot(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if "ps_parking_lot_" in button_id:
        print(f'ps_parking lot button_id: {button_id}')
        return [button_id]
    else:
        #print(f'submit button_id: {button_id}')
        raise PreventUpdate
        #return [button_id]
 
lot_buttons = [f'ps_parking_lot_{i * 3 + j + 1}' for i in range(5) for j in range(3)]


@app.callback(
    #[Output(f'parking_lot_{i * 3 + j + 1}', 'style') for i in range(5) for j in range(3)],
    #[Output(button_id,'style') for button_id in lot_buttons],
    [Output(button_id,'disabled') for button_id in lot_buttons],
    [
        Input('ps_date_picker','date'),
        Input('ps_floor','value'),
        Input('ps_time_picker_start','value'),
        Input('ps_time_picker_end','value'),
    ],
)
def update_parking_lot_availability(date, floor, park_time_start, park_time_end):
    if not date or not floor or not park_time_start or not park_time_end:
        raise PreventUpdate
    
    print(f'floor update parking lot avail: {floor}')
    #if floor:
    #    floor = str(floor).replace("Level ", "")

    print(f'parking start time: {park_time_start}')
    sql = """
        SELECT
            booking.parking_id
            ,parking_slot.lot_no
        FROM booking
        LEFT JOIN parking_slot
        ON booking.parking_id = parking_slot.parking_id
        WHERE TO_CHAR(booking_date,'YYYY-MM-DD') = %s
        AND end_date <= %s
        AND start_date >= %s
        AND floor = %s
    """
    print(f"Date:{date}")
    print(f"park_time_start: {park_time_start}")
    print(f"park_time_end: {park_time_end}")
    print(f"floor:{floor}")
    values = [date, park_time_start, park_time_end, floor]
    cols = ['parking_id','lot_no']

    result = db.querydatafromdatabase(sql,values,cols)
    if result.empty:
        print(f'Empty')
        raise PreventUpdate
    result2 = result['lot_no'][0]
    print(f'result: {result2}')
    unavailable_parking = result['lot_no'][0].tolist()
    unavailable_parking = str(unavailable_parking)
    print(f'unavailable parking: {unavailable_parking}')

    #button_styles = []
    button_states = []
    for button_id in lot_buttons:
        lot_no = button_id.replace("ps_parking_lot_","")
        if lot_no in unavailable_parking:
            #button_styles.append({'backgroundColor':'gainsboro','border':'gainsboro','color':'black','margin': '5px', 'width':'75px'})
            button_states.append(True)
        else:
            #button_styles.append({'backgroundColor':'info', 'color':'white','margin': '5px', 'width':'75px'})
            button_states.append(False)
    #return button_styles, button_states
    return button_states


@app.callback(
    [
        Output('ps_booking_modal','is_open'),
    ],
    [
        Input('ps_submit', 'n_clicks'),
        Input('url', 'pathname'),
        Input('ps_selected_parking_lot', 'data'),
        Input("close","n_clicks"),
    ],
    [
        State('ps_date_picker', 'date'),
        State('ps_floor', 'value'),
        State('ps_time_picker_start','value'),
        State('ps_time_picker_end','value'),
        State('url','search'),
        #State('approval-trigger','data')
    ]
    
)
def handle_submit(submitbtn, pathname, selected_lot,close_clicks,date, floor, park_start, park_end, search):
    ctx = dash.callback_context
    if not ctx.triggered:
        print(f'Not working')
        raise PreventUpdate
    

    print(f'Working')
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'close':
            return [False]
    print(f'ps_submit_button_id: {button_id}')

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'ps_submit' or not submitbtn:
        print(f"Different event")
        raise PreventUpdate
    
    parsed = urlparse(search)

    user_id = parse_qs(parsed.query).get('id', [None])[0]

    if selected_lot:
        selected_lot = selected_lot.replace("ps_parking_lot_", "")

    print(f"user_id: {user_id}, selected_lot: {selected_lot}, date: {date}, floor: {floor}, park_start: {park_start}, park_end: {park_end}")

    sql = "SELECT MAX(booking_id) AS max_booking_id FROM booking"
    values = []
    cols = ['booking_id']
    result = db.querydatafromdatabase(sql, values, cols)
    max_booking_no = result['booking_id'].iloc[0] + 1 if pd.notna(result['booking_id'].iloc[0]) else 1

    sql2 = """
        SELECT
            registration_no
        FROM registration
        WHERE customer_id = %s
    """
    values_2 = [user_id]
    cols_2 = ['registration_no']
    result_2 = db.querydatafromdatabase(sql2,values_2,cols_2)
    reg_no = result_2['registration_no'].iloc[0]

    sql3 = """
        SELECT
            parking_id
            ,floor
            ,lot_no
        FROM parking_slot
        WHERE floor = %s
        AND lot_no = %s
    """
    values_3 = [floor, selected_lot]
    cols_3 = ['parking_id','floor','lot_no']
    result_3 = db.querydatafromdatabase(sql3, values_3,cols_3)
    parking_id = result_3['parking_id'].iloc[0]

    sql4 = """
        INSERT INTO booking(booking_id, registration_no, parking_id, booking_date, start_date, end_date,is_advanced_booking)
        VALUES(%s, %s,%s,%s,%s,%s,%s)
    """
    values_4 = [str(max_booking_no),str(reg_no),str(parking_id),date,park_start, park_end,False]
    db.modifydatabase(sql4,values_4)

    sql5 = """
        SELECT MAX(payment_id)
        FROM booking_payment
    """
    values_5 = []
    cols_5 = ['payment_id']
    result_5 = db.querydatafromdatabase(sql5,values_5,cols_5)
    max_payment_id = result_5['payment_id'].iloc[0] + 1 if pd.notna(result_5['payment_id'].iloc[0]) else 1

    sql6 = """
        INSERT INTO booking_payment(payment_id, payment_status, payment_amount, booking_id)
        VALUES(%s, %s, %s, %s)
    """
    values_6 = [str(max_payment_id),False,100,str(max_booking_no)]
    cols_6 = ['payment_id','payment_status','payment_amount','booking_id']
    result_6 = db.modifydatabase(sql6,values_6)

    return [True]

@app.callback(
    [
        Output('ps_customer_image_result', 'src'),
        Output('ps_customer_name', 'children'),
        Output('ps_customer_created_date', 'children'),
        Output('ps_customer_approval_date', 'children'),
        Output('ps_customer_car_brand', 'children'),
        Output('ps_customer_car_model', 'children'),
        Output('ps_customer_plate_number', 'children'),
        Output('ps_ytd_advanced_booking', 'children'),
        Output('ps_mtd_advanced_booking', 'children'),
        Output('ps_booked_parking', 'children')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def advanced_book_customerprofile_load(pathname, search):
    if pathname == '/parking_selection/new/book':
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
                TO_CHAR(booking_date,'YYYY-MM') AS year
                ,customer_id
                ,COUNT(DISTINCT booking_id) AS booking_count
            FROM booking
            LEFT JOIN registration
            ON booking.registration_no = registration.registration_no
            WHERE customer_id = %s
            AND TO_CHAR(booking_date,'YYYY-MM') = TO_CHAR(CURRENT_TIMESTAMP,'YYYY-MM')
            AND is_advanced_booking = False
            GROUP BY
                TO_CHAR(booking_date,'YYYY-MM')
                ,customer_id 
            """
            values_3 = [user_id]
            cols3 = ['booking_year','customer_id','booking_count']
            result3 = db.querydatafromdatabase(sql3,values_3,cols3)
            if result3.empty:
                mtd_count = 0
            else:
                mtd_count = result3['booking_count'].iloc[0]
                #mtd_count = str(mtd_count)
            print(f'Result mtd:{mtd_count}')

            mtd_booked_parking = 5 - mtd_count
            return image, name, f"Registration Date: {created_date}", f"Approval Date: {approval_date}", f"Car Brand: {car_brand}", f"Car Model: {car_model}", f"Plate No.: {plate_number}", f"{ytd_count}",  f"{mtd_count}", f"{mtd_booked_parking}"
            #return name, f"Registered Date: {created_date}"
    else:
        raise PreventUpdate

