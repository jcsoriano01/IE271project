from dash import dcc
from dash import html
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
        
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        html.H4('Customer Information')
                                        ,html.Hr()
                                        ,dbc.Alert(id = 'signup_alert', is_open=False)
                                        ,dbc.Col(
                                                [
                                                    dbc.Label("Type")
                                                    ,dbc.RadioItems(
                                                        id = 'signup_type'
                                                        ,options=[
                                                            {'label':"Customer", 'value':1}
                                                            ,{'label':"Employee", 'value':2},
                                                            ]
                                                        ,inline=True
                                                    ),
                                                ]
                                                ,width = 6
                                        )
                                        ,dbc.Col(
                                                [
                                                    dbc.Label("Is Active")
                                                    ,dbc.RadioItems(
                                                        id = 'signup_isactive'
                                                        ,options=[
                                                            {'label':"Yes", 'value':True}
                                                            ,{'label':"No", 'value':False},
                                                            ]
                                                        ,inline=True
                                                    )
                                                ]
                                                ,width = 6
                                        )
                                    ]
                                    ,className='mb-3'
                                )
                                ,dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Label('Given Name', width=12)
                                                ,dbc.Input(
                                                    type='text'
                                                    ,id='signup_givenname'
                                                    ,placeholder='Given Name'
                                                )
                                            ]
                                            ,width=3
                                        )
                                        ,dbc.Col(
                                            [
                                                dbc.Label('Middle Name', width=12)
                                                ,dbc.Input(
                                                    type='text'
                                                    ,id='signup_middlename'
                                                    ,placeholder='Middle Name'
                                                )
                                            ]
                                            ,width=3
                                        )
                                        ,dbc.Col(
                                            [
                                                dbc.Label('Surname', width=12)
                                                ,dbc.Input(
                                                    type='text'
                                                    ,id='signup_surname'
                                                    ,placeholder='Surname'
                                                )
                                            ]
                                            ,width=3
                                        )
                                        ,dbc.Col(
                                            [
                                                dbc.Label('Suffix', width=12)
                                                ,dbc.Input(
                                                    type='text'
                                                    ,id='signup_suffix'
                                                    ,placeholder='Suffix'
                                                )
                                            ]
                                            ,width=3
                                        )
                                    ]
                                    ,className='mb-3'
                                )
                                ,dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Label('Image', width=12, style={'display': 'inline-block', 'verticalAlign': 'middle'})
                                                ,dcc.Upload(
                                                    id='signup_image'
                                                    ,children=html.Div(
                                                        ['Select Files']
                                                    )
                                                    ,style={
                                                        'width': '80%'
                                                        ,'height': '30px'
                                                        ,'lineHeight': '30px'
                                                        ,'borderWidth': '1px'
                                                        ,'borderStyle': 'dashed'
                                                        ,'borderRadius': '5px'
                                                        ,'textAlign': 'center'
                                                        ,'margin': '10px'
                                                        ,'display': 'inline-block'
                                                    }
                                                    ,multiple=False
                                                )
                                                ,html.Div(id='output-image-upload')
                                                ,html.Img(id='signup_image_preview', style={'width': '150px', 'height': '150px', 'object-fit': 'cover'})
                                            ]
                                            ,width=6
                                        )
                                        ,dbc.Col(
                                            [
                                                dbc.Label("Driver's Licence", width=12, style={'display': 'inline-block', 'verticalAlign': 'middle'})
                                                ,dcc.Upload(
                                                    id='signup_license'
                                                    ,children=html.Div(
                                                        ['Select Files']
                                                    )
                                                    ,style={
                                                        'width': '80%'
                                                        ,'height': '30px'
                                                        ,'lineHeight': '30px'
                                                        ,'borderWidth': '1px'
                                                        ,'borderStyle': 'dashed'
                                                        ,'borderRadius': '5px'
                                                        ,'textAlign': 'center'
                                                        ,'margin': '10px'
                                                        ,'display': 'inline-block'
                                                    }
                                                    ,multiple=False
                                                )
                                                ,html.Div(id='output-license-upload')
                                                ,html.Img(id='signup_license_preview', style={'width': '150px', 'height': '150px', 'object-fit': 'cover'})
                                            ]
                                            ,width=6
                                        )
                                    ]
                                    ,className="mb-3"
                                )
                            ]
                            ,width = 6
                            ,style={
                                'backgroundColor': "#FFFFFF",
                                'padding': '20px',
                                'borderRadius': '5px',
                                'minHeight': 'auto',
                                'border': '1px solid #ced4da',
                                'fontFamily': 'Georgia',
                                'marginRight':'auto'
                            }
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        html.H4('Employment Information')
                                        ,html.Hr()
                                        ,dbc.Col(
                                                    [
                                                        dbc.Label("Employment Date",width = 12)
                                                        ,dcc.DatePickerSingle(
                                                            id='signup_employment_date',
                                                            min_date_allowed=datetime(1995, 8, 5),
                                                            max_date_allowed=datetime(2024, 9, 19),
                                                            initial_visible_month=datetime(2024, 1, 1),
                                                            date=str(datetime(2024, 1, 1).date()),
                                                            display_format='YYYY-MM-DD',
                                                            style={'width': '100%'}
                                                        )
                                                ],
                                                width=4
                                            )
                                        ,dbc.Col(
                                                    [
                                                        dbc.Label('Job Title', width=12)
                                                        ,dbc.Input(
                                                            type='text'
                                                            ,id='signup_title'
                                                        )
                                                    ]
                                                    ,width=4
                                        )
                                        ,dbc.Col(
                                                    [
                                                        dbc.Label('Department', width=12)
                                                        ,dbc.Input(
                                                            type='text'
                                                            ,id='signup_department'
                                                        )
                                                    ]
                                                    ,width=4
                                        )
                                    ]
                                )
                                ,html.Br()
                                ,dbc.Row(
                                    [
                                        html.H4('Vehicle Information')
                                        ,html.Hr()
                                        ,dbc.Col(
                                            [
                                                dbc.Label('Plate Number', width = 'auto')
                                                ,dbc.Input(
                                                            type='text',
                                                            id='signup_plate_no',
                                                            placeholder='Plate Number'
                                                        )
                                            ]
                                            ,width = 4
                                        )
                                        ,dbc.Col(
                                            [
                                                dbc.Label('Car Brand', width = 'auto')
                                                ,dbc.Input(
                                                            type='text',
                                                            id='signup_car_brand',
                                                            placeholder='Car Brand'
                                                        )
                                            ]
                                            ,width = 4
                                        )
                                        ,dbc.Col(
                                            [
                                                dbc.Label('Car Model', width = 'auto')
                                                ,dbc.Input(
                                                            type='text',
                                                            id='signup_car_model',
                                                            placeholder='Car Model'
                                                        )
                                            ]
                                            ,width = 4
                                        )

                                    ]
                                )
                                ,html.Br()
                                ,html.Br()
                                ,dbc.Row(
                                    [
                                        html.H4('Access Information')
                                        ,html.Hr()
                                        ,dbc.Col(
                                            [
                                                dbc.Label('Username', width = 'auto')
                                                ,dbc.Input(
                                                            type='text',
                                                            id='signup_username',
                                                        )
                                            ]
                                            ,width = 6
                                        )
                                        ,dbc.Col(
                                            [
                                                dbc.Label('Password', width = 'auto')
                                                ,dbc.Input(
                                                    type='password', id='signup_password'
                                                ),
                                            ]
                                            ,width = 6
                                        )
                                    ]
                                )
                            ]
                            ,width = 6
                            ,style={
                                'backgroundColor': "#FFFFFF",
                                'padding': '20px',
                                'borderRadius': '5px',
                                'minHeight': 'auto',
                                'border': '1px solid #ced4da',
                                'fontFamily': 'Georgia',
                                'marginLeft': 'auto'
                            }
                        )
                    ]
                    ,style={
                                'backgroundColor': "#FFFFFF",
                                'padding': '20px',
                                'borderRadius': '5px',
                                'minHeight': 'auto',
                                #'border': '1px solid #ced4da',
                                'fontFamily': 'Georgia'
                            }
                )
            ]
        )
        ,dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    'Your record has been submitted for approval'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed"
                        ,href = '/'
                    )
                )
            ]
            ,centered=True
            ,id = 'signup_successmodal'
            ,backdrop='static'
        )
        ,html.Br()
        ,dbc.Button(
            'Submit'
            ,id = 'signup_submit'
            ,n_clicks=0
        )
    ]
)

@app.callback(
    [
        Output('signup_alert', 'color'),
        Output('signup_alert', 'children'),
        Output('signup_alert', 'is_open'),
        Output('signup_successmodal', 'is_open'),
    ],
    [   Input('signup_submit', 'n_clicks')
        ,Input('url', 'pathname') 
    ],
    [
        State('signup_type', 'value'),
        State('signup_givenname', 'value'),
        State('signup_middlename', 'value'),
        State('signup_surname', 'value'),
        State('signup_suffix', 'value'),
        State('signup_image', 'contents'),
        State('signup_license', 'contents'),
        State('signup_plate_no', 'value'),
        State('signup_car_brand', 'value'),
        State('signup_car_model', 'value'),
        State('signup_isactive', 'value'),
        State('signup_username', 'value'),
        State('signup_password', 'value'),
        State('signup_employment_date','date'),
        State('signup_title','value'),
        State('signup_department','value'),
        State('url', 'search')
    ]
)
def signup_saveprofile(submitbtn, pathname, type, givenname, middlename, surname, suffix, image_contents, license_contents, plate_no, car_brand, car_model, is_active,username, password,employment_date,title,department,search):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'signup_submit' or not submitbtn:
        raise PreventUpdate

    parsed = urlparse(search)
    #create_mode = parse_qs(parsed.query)['mode'][0]
    query_params = parse_qs(parsed.query)
    create_mode = query_params.get('mode', [None])[0]
    
    # Set default outputs
    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''

    # Check inputs
    if not type:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Please select user type.'
    elif not givenname:
        alert_open = True
        alert_color = 'danger'
        alert_text = "Please provide customer's given name."
    elif not surname:
        alert_open = True
        alert_color = 'danger'
        alert_text = "Please provide customer's surname."
    elif not plate_no:
        alert_open = True
        alert_color = 'danger'
        alert_text = "Please provide your car's plate number."
    elif not car_brand:
        alert_open = True
        alert_color = 'danger'
        alert_text = "Please provide your car's brand."
    elif not car_model:
        alert_open = True
        alert_color = 'danger'
        alert_text = "Please provide your car's model."
    elif not username and type == 2:
        alert_open = True
        alert_color = 'danger'
        alert_text = "Please provide your username."
    elif not password and type == 2:
        alert_open = True
        alert_color = 'danger'
        alert_text = "Please provide your password."
    else:
        sql1 = "SELECT MAX(user_id) AS max_user_id FROM users"
        values = []
        cols = ['user_id']
        result = db.querydatafromdatabase(sql1, values, cols)
        max_userid = result['user_id'].iloc[0]

        sql2 = "SELECT MAX(registration_no) AS max_reg_no FROM registration"
        values = []
        cols = ['registration_no']
        result2 = db.querydatafromdatabase(sql2, values, cols)
        max_regno = result2['registration_no'].iloc[0] if pd.notna(result2['registration_no'].iloc[0]) else 0

        
        if image_contents:
            # image_contents is a base64 encoded string starting with "data:image/jpeg;base64,"
            image_data = base64.b64decode(image_contents.split(',')[1])
        else:
            image_data = None

        if license_contents:
            # image_contents is a base64 encoded string starting with "data:image/jpeg;base64,"
            license_data = base64.b64decode(license_contents.split(',')[1])
        else:
            license_data = None

        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        sql = """
            INSERT INTO users (user_id, firstname, middlename, lastname, created_date, role_id, is_active, image, drivers_license, suffix)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = [int(max_userid)+1, givenname, middlename, surname, current_timestamp, type, is_active, image_data, license_data, suffix]
        db.modifydatabase(sql, values)

        sql1 = """
            INSERT INTO registration (registration_no, registration_date, registration_status_id, customer_id, plate_number, car_brand, car_model)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values1 = [int(max_regno)+1, current_timestamp, 1, int(max_userid)+1, plate_no, car_brand, car_model]
        db.modifydatabase(sql1, values1)

        print(f'type: {type}')
        if type == 2:
            sql2 = """
                INSERT INTO employees(user_id, employment_date, registration_no, user_name, user_password, job_title, department)
                VALUES(%s,%s,%s,%s,%s,%s,%s)
            """
            values2 = [int(max_userid)+1,employment_date,int(max_regno)+1,username,password,title,department]
        modal_open = True
    return [alert_color, alert_text, alert_open, modal_open]


