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
        html.Div(
            [
                dcc.Store(id = 'customerprofile_toload', storage_type='memory', data =0),
            ]
        )
        ,html.H4('Customer Information')
        ,html.Hr()
        ,dbc.Alert(id = 'customerprofile_alert', is_open=False)
        ,dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Col(
                                "Type"
                                ,width = 1
                        )
                        ,dbc.Col(
                                dbc.RadioItems(
                                    id = 'customerprofile_type'
                                    ,options=[
                                        {'label':"Customer", 'value':1}
                                        ,{'label':"Employee", 'value':2},
                                        ]
                                    ,inline=True
                                ),
                                width = 5
                        )
                        ,dbc.Col(
                                "Is Active"
                                ,width = 1
                        )
                        ,dbc.Col(
                                [
                                    dbc.RadioItems(
                                    id = 'customerprofile_isactive'
                                    ,options=[
                                        {'label':"Yes", 'value':True}
                                        ,{'label':"No", 'value':False},
                                        ]
                                    ,inline=True
                                )
                                ]
                                ,width = 5
                        ),
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
                                    ,id='customerprofile_givenname'
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
                                    ,id='customerprofile_middlename'
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
                                    ,id='customerprofile_surname'
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
                                    ,id='customerprofile_suffix'
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
                                dbc.Label('Image', width=3, style={'display': 'inline-block', 'verticalAlign': 'middle'})
                                ,dcc.Upload(
                                    id='customerprofile_image'
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
                                ,html.Img(id='customerprofile_image_preview', style={'width': '150px', 'height': '150px', 'object-fit': 'cover'})
                            ]
                            ,width=6
                        )
                        ,dbc.Col(
                            [
                                dbc.Label("Driver's Licence", width=3, style={'display': 'inline-block', 'verticalAlign': 'middle'})
                                ,dcc.Upload(
                                    id='customerprofile_license'
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
                                ,html.Img(id='customerprofile_license_preview', style={'width': '150px', 'height': '150px', 'object-fit': 'cover'})
                            ]
                            ,width=6
                        )
                    ]
                    ,className="mb-3"
                )
            ]
        )
        ,html.H4('Vehicle Information')
        ,html.Hr()
        ,dbc.Form(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label('Plate Number', width = 'auto')
                            ,dbc.Input(
                                        type='text',
                                        id='customerprofile_plate_no',
                                        placeholder='Plate Number'
                                    )
                        ]
                    )
                    ,dbc.Col(
                        [
                            dbc.Label('Car Brand', width = 'auto')
                            ,dbc.Input(
                                        type='text',
                                        id='customerprofile_car_brand',
                                        placeholder='Car Brand'
                                    )
                        ]
                    )
                    ,dbc.Col(
                        [
                            dbc.Label('Car Model', width = 'auto')
                            ,dbc.Input(
                                        type='text',
                                        id='customerprofile_car_model',
                                        placeholder='Car Model'
                                    )
                        ]
                    )
                ]
                ,className="mb-3"
            )
        )
        ,html.Hr()
        ,dbc.Button(
            'Submit'
            ,id = 'customerprofile_submit'
            ,n_clicks=0
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
                        ,href = '/customer_registration'
                    )
                )
            ]
            ,centered=True
            ,id = 'customerprofile_successmodal'
            ,backdrop='static'
        )
        ,dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Edit Saved')
                ),
                dbc.ModalBody(
                    'Your changes has been successfully saved.'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed"
                        ,href = '/customer_registration'
                    )
                )
            ]
            ,centered=True
            ,id = 'customerprofile_editsuccessmodal'
            ,backdrop='static'
        )
    ]
    ,style={'font-family':'Georgia','color':'#696969'}
)

from dash.exceptions import PreventUpdate
import dash

@app.callback(
    [
        Output('customerprofile_alert', 'color'),
        Output('customerprofile_alert', 'children'),
        Output('customerprofile_alert', 'is_open'),
        Output('customerprofile_successmodal', 'is_open'),
        Output('customerprofile_editsuccessmodal','is_open'),
    ],
    [   Input('customerprofile_submit', 'n_clicks')
        ,Input('url', 'pathname') 
    ],
    [
        State('customerprofile_type', 'value'),
        State('customerprofile_givenname', 'value'),
        State('customerprofile_middlename', 'value'),
        State('customerprofile_surname', 'value'),
        State('customerprofile_suffix', 'value'),
        State('customerprofile_image', 'contents'),
        State('customerprofile_license', 'contents'),
        State('customerprofile_plate_no', 'value'),
        State('customerprofile_car_brand', 'value'),
        State('customerprofile_car_model', 'value'),
        State('customerprofile_isactive', 'value'),
        State('url', 'search')
    ]
)
def customerprofile_saveprofile(submitbtn, pathname, type, givenname, middlename, surname, suffix, image_contents, license_contents, plate_no, car_brand, car_model, is_active,search):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'customerprofile_submit' or not submitbtn:
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
    modal_edit = False
    
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
    elif create_mode == 'edit':
        user_id = parse_qs(parsed.query)['id'][0]

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


        sql2 = """
        UPDATE users
            SET 
                firstname = %s
                ,middlename = %s
                ,lastname = %s
                ,role_id = %s
                ,image = %s
                ,drivers_license = %s
                ,suffix = %s
                ,is_active = %s
            WHERE user_id = %s
        """
            
            
        
        values2 = [givenname, middlename, surname, type, image_data, license_data, suffix, is_active, user_id]
        db.modifydatabase(sql2, values2)

        sql3 = """
            UPDATE registration
            SET
                plate_number = %s
                ,car_brand = %s
                ,car_model = %s
            WHERE customer_id = %s
        """
        values3 = [plate_no, car_brand, car_model, user_id]
        db.modifydatabase(sql3, values3)
        modal_open = False
        modal_edit = True

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

        modal_open = True
        modal_edit = False
    return [alert_color, alert_text, alert_open, modal_open, modal_edit]

@app.callback(
    [
        Output('customerprofile_type', 'value'),
        Output('customerprofile_givenname', 'value'),
        Output('customerprofile_middlename', 'value'),
        Output('customerprofile_surname', 'value'),
        Output('customerprofile_suffix', 'value'),
        #Output('customerprofile_image', 'contents'),
        #Output('customerprofile_license', 'contents'),
        Output('customerprofile_image_preview', 'src'),
        Output('customerprofile_license_preview', 'src'),
        Output('customerprofile_plate_no', 'value'),
        Output('customerprofile_car_brand', 'value'),
        Output('customerprofile_car_model', 'value'),
        Output('customerprofile_isactive', 'value'),
    ],
    [
        #Input('customerprofile_toload', 'modified_timestamp'),
        #Input('url','pathname')
        Input('url', 'pathname')
    ],
    [#State('customerprofile_toload', 'data'), 
     State('url', 'search')]
)
#def customerprofile_load(timestamp, search):
def customerprofile_load(pathname, search):
    if pathname == "/customer_registration/new":
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0

        if to_load == 1:
        #parsed = urlparse(search)
            user_id = parse_qs(parsed.query)['id'][0]

            if not user_id:
                raise PreventUpdate

            sql = """
                SELECT
                    role_id AS type,
                    firstname AS givenname,
                    middlename,
                    lastname AS surname,
                    suffix,
                    image,
                    drivers_license AS license,
                    plate_number AS plate_no,
                    car_brand,
                    car_model,
                    is_active
                FROM users
                LEFT JOIN registration
                ON users.user_id = registration.customer_id
                WHERE users.user_id = %s
            """
            values = [user_id]
            col = ['type', 'givenname', 'middlename', 'surname', 'suffix', 'image', 'license', 'plate_no', 'car_brand', 'car_model','is_active']
        
            df = db.querydatafromdatabase(sql, values, col)

            if df.empty:
                raise PreventUpdate

            # Extract values from the DataFrame
        
            type = int(df['type'][0])
            givenname = df['givenname'][0]
            middlename = df['middlename'][0]
            surname = df['surname'][0]
            suffix = df['suffix'][0]
            image_data = df['image'][0]
            license_data = df['license'][0]
            plate_no = df['plate_no'][0]
            car_brand = df['car_brand'][0]
            car_model = df['car_model'][0]
            is_active = df['is_active'][0]

            image = f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}" if image_data else None
            license = f"data:image/png;base64,{base64.b64encode(license_data).decode('utf-8')}" if license_data else None

            return [type,givenname,middlename,surname,suffix,image,license,plate_no,car_brand,car_model,is_active]
    else:
        raise PreventUpdate
