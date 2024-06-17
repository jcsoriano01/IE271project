from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL
from urllib.parse import urlparse, parse_qs
import base64

from app import app
from apps import dbconnect as db
from datetime import datetime

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H4(
                                ["Welcome!"],
                                style= {
                                    #'color': '#B82601',
                                    'color':'#696969',
                                    'margin': '0 10px',
                                    'font-family': 'Georgia',
                                }    
                                ),
                            html.Hr(),
                            #html.Img(src="/assets/image.jpg", style={'display': 'block', 'margin': 'auto','width': '50%', 'height': 'auto'}),
                            html.Div(
                                html.Img(id='home_customer_image',
                                style={'display': 'block', 'margin': 'auto', 'width': '50%', 'height': 'auto'})
                            ),
                            html.Br(),
                            html.H5(
                                #["Jhon Cris Soriano"]
                                [
                                    html.Div(
                                        id = 'home_user_name'
                                        ,style = {
                                            'textAlign': 'center',
                                            'margin': '0'
                                        }
                                    )
                                ]
                                ),
                            html.P(
                                #['Customer Parking Supervisor']
                                id = 'home_job_title'
                                ,style= {
                                    'textAlign':'center',
                                    'font-style':'italic',
                                    'color':'#6B8E23'
                                }
                            ),
                            html.P(
                                #['Property Management']
                                id = 'home_user_department'
                                ,style= {
                                    'textAlign':'center',
                                    'color':'#696969'
                                }
                            )
                        ],
                        style= {
                            'backgroundColor':"#FFFFFF",
                            'padding':'20px',
                            'borderRadius':'5px',
                            #'minHeight':'100vh',
                            'minHeight':'auto',
                            'border': '1px solid #ced4da',
                            'font-family':'Georgia'
                        }    
                    ),
                    width=3
                ),
                dbc.Col(
                        html.Div(
                            [
                                html.H4(["Announcement"]
                                ,style= {
                                    #'color': '#B82601',
                                    'color':'#696969',
                                    'margin': '0 10px',
                                    'font-family': 'Georgia',
                                }       
                                )
                                ,html.Hr()
                                ,dbc.Carousel(
                                    items=[
                                        {"key": "1", "src": "/assets/TRUST makes.jpg",'img_style':{'object-fit':'cover',"max-height":"250px"}, 'imgClassName':'w-100'},
                                        {"key": "2", "src": "/assets/recognition.jpg", 'img_style':{'object-fit':'cover',"max-height":"250px"}, 'imgClassName':'w-100'},
                                        {"key": "3", "src": "/assets/success.jpg", 'img_style':{'object-fit':'cover',"max-height":"250px"}, 'imgClassName':'w-100'},
                                    ],
                                    controls=False,
                                    indicators=False,
                                    interval=5000,
                                    ride="carousel",
                                )
                            ],
                            style= {
                            'backgroundColor':"#FFFFFF",
                            'padding':'20px',
                            'borderRadius':'5px',
                            'minHeight':'50vh',
                            'border': '1px solid #ced4da',
                            'font-family':'Georgia'
                            }
                        )
                        ,width=6
                    )
                ,dbc.Col(
                    html.Div(
                        [
                            html.H4(["Worklist"]
                                ,style= {
                                    #'color': '#B82601',
                                    'color':'#696969',
                                    'margin': '0 10px',
                                    'font-family': 'Georgia',
                                }       
                                )
                            ,html.Hr()
                            ,dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H6('For Approval - New Records',className='card-title')
                                        ,html.Div(
                                            id = 'home_for_approval'
                                            ,style={
                                                'display': 'flex', 
                                                'align-items': 'center', 
                                                'justify-content': 'center', 
                                                'color': "darkgreen",
                                                'font-size': '48px',  # Adjust the font size as needed
                                                'font-weight': 'bold'  # Make the text bold
                                            },
                                            className='card-title',
                                        )
                                    ]
                                ),
                                className = 'w-80'
                                ,color='chartreuse'
                                ,style= {
                                    #'color': '#B82601',
                                    'color':'#696969',
                                    'margin': '0 10px',
                                    'font-family': 'Georgia',
                                    'align':'center'
                                }    
                            )
                            ,html.Br()
                            ,dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H6('For Approval - New Records',className='card-title')
                                        ,html.Div(
                                            id = 'home_for_approval_ab'
                                            ,style={
                                                'display': 'flex', 
                                                'align-items': 'center', 
                                                'justify-content': 'center', 
                                                'color': "teal",
                                                'font-size': '48px',  # Adjust the font size as needed
                                                'font-weight': 'bold'  # Make the text bold
                                            },
                                            className='card-title',
                                        )
                                    ]
                                ),
                                className = 'w-80'
                                ,color='lavender'
                                ,style= {
                                    #'color': '#B82601',
                                    'color':'#696969',
                                    'margin': '0 10px',
                                    'font-family': 'Georgia',
                                    'align':'center'
                                }    
                            )
                        ]
                        ,style={
                            'backgroundColor': "#FFFFFF",
                            'padding': '20px',
                            'borderRadius': '5px',
                            'minHeight': '50vh',
                            'border': '1px solid #ced4da',
                            'font-family': 'Georgia'
                        }
                    )
                    ,width=3
                )
            ]
        )
        #html.Img(src='/assets/your-image-file.jpg', style={'display': 'block', 'margin': '20px auto'}),  # Placeholder image URL
    ],
    style={'backgroundColor': '#FFFFF0'}
)

@app.callback(
    [
        Output('home_user_name','children'),
        Output('home_job_title','children'),
        Output('home_user_department','children'),
        Output('home_customer_image', 'src'),
    ],
    [
        Input('url','pathname'),
        State('currentuserid','data'),
    ]
)
def customers_home_profile(pathname,user_id):
    if pathname == '/' or pathname == '/home':
        sql = """
            SELECT
                a.user_id
                ,(b.firstname || ' ' || b.lastname) AS customer_name
                ,a.job_title
                ,a.department
                ,b.image
            FROM employees a
            LEFT JOIN users b
            ON a.user_id = b.user_id
            WHERE a.user_id = %s
        """
        values = [user_id]
        cols = ['user_id','customer_name','job_title','department','image']
        result = db.querydatafromdatabase(sql,values,cols)

        print(f'user_id: {user_id}')

        customer_name = result['customer_name']
        job_title = result['job_title'].iloc[0]
        department = result['department'].iloc[0]
        image_data = result['image'].iloc[0]

        image = f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}" if image_data else None
        print(f'customer name: {customer_name}')
        print(f'job_title: {job_title}')
        print(f'department: {department}')

        return [customer_name, job_title, department, image]
    else:
        raise PreventUpdate




@app.callback(
    [
        Output('home_for_approval','children'),
        Output('home_for_approval_ab','children'),
    ],
    [
        Input('url','pathname'),
        #Input('approval-trigger','data'),
    ]
)
def customers_for_approval_count(pathname):
    if pathname == '/' or pathname == '/home':
        sql = """
        SELECT
            COUNT(DISTINCT CASE WHEN b.registration_status_id = 1 THEN user_id END) AS count_approval
            ,COUNT(DISTINCT CASE WHEN b.registration_status_id = 2 AND is_adv_booking_apprv = 1 THEN booking_id END) AS ab_count_approval
        FROM users a
        JOIN registration b ON a.user_id = b.customer_id
        JOIN registration_status c ON b.registration_status_id = c.registration_status_id
        LEFT JOIN booking d
        ON b.registration_no = d.registration_no
        WHERE is_active = true
        """ 
        values = []

        cols = ['count_approval','ab_count_approval']
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0] >0:
            count = df['count_approval'].iloc[0]
            ab_count = df['ab_count_approval'].iloc[0]
            return count, ab_count
        else:
            return "0","0"
        
        
    else:
        return "0","0"
