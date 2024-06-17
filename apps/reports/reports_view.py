import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    id='gauge_chart',
                                    style={'height': '40vh', 'width':'100%'}  # Set the height for the gauge chart
                                ),
                                width=12
                            ),
                            style={'margin-bottom': '0.5px'}  # Add margin between rows
                        ),
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    id='gauge_chart__available_slots',
                                    style={'height': '40vh','width':'100%'}  # Set the height for the available slots chart
                                ),
                                width=12
                            ),
                            style={'margin-bottom': '0.5px'}
                        ),
                        # dbc.Row(
                        #     dbc.Col(
                        #         dcc.Graph(
                        #             id='gauge_chart__adv_booking',
                        #             style={'height': '45vh','width':'100%'}  # Set the height for the available slots chart
                        #         ),
                        #         width=12
                        #     ),
                        #     style={'margin-bottom': '0.5px'}
                        # )
                    ],
                    width=3
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
                                                        [html.H5("MTD Total Booking", style={'margin': 0})],
                                                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px','background-color':'primary','fontFamily': 'Georgia'}
                                                    ),
                                                    dbc.CardBody(
                                                        [
                                                            html.Div(
                                                                "0",
                                                                id='reports_mtd_total_booking',
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
                                                                id='reports_mtd_advanced_booking',
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
                                    ),dbc.Col(
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
                                                                id='reports_avg_parking_duration',
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
                                    )
                            ]
                        )
                        ,html.Br()
                        ,dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                        id='bar_chart_parking_volume',
                                        style={'height': '40vh', 'width':'100%','border': '1px solid #ced4da',}  # Set the height for the gauge chart
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
    ,style={
                'backgroundColor': "#FFFFFF",
                'padding': '20px',
                'borderRadius': '5px',
                'minHeight': 'auto',
                #'border': '1px solid #ced4da',
                'fontFamily': 'Georgia'
            }
)

@app.callback(
    [
        Output('gauge_chart','figure'),
        Output('gauge_chart__available_slots','figure'),
        Output('reports_mtd_total_booking','children'),
        Output('reports_mtd_advanced_booking','children'),
        Output('reports_avg_parking_duration','children'),
        Output('bar_chart_parking_volume','figure'),
        #Output('gauge_chart__adv_booking','figure'),
    ],
    [
        Input('url', 'pathname'),
    ]
)
def occupancy_rate(pathname):
    if pathname == '/reports':
        sql = """
        SELECT
            COUNT(DISTINCT booking.parking_id) AS occupied_parking
        FROM booking
        LEFT JOIN parking_slot
        ON booking.parking_id = parking_slot.parking_id
        WHERE TO_CHAR(booking_date,'YYYY-MM-DD') = TO_CHAR(CURRENT_TIMESTAMP,'YYYY-MM-DD')
        AND end_date >= TO_CHAR(CURRENT_TIMESTAMP,'HH24:MI')
        AND start_date <= TO_CHAR(CURRENT_TIMESTAMP,'HH24:MI')
        """
        values = []
        cols = ['occupied_parking']
        result = db.querydatafromdatabase(sql,values,cols)
        occupied = result['occupied_parking'].iloc[0]

        sql2 = """
        SELECT
            COUNT(DISTINCT parking_id) AS parking_count
        FROM parking_slot
        """
        values2 = []
        cols2 = ['parking_count']
        result2 = db.querydatafromdatabase(sql2,values2,cols2)
        total_parking = result2['parking_count'].iloc[0]
        occupancy_rate = (occupied/total_parking)*100
        print(f'Occupied: {occupied}')
        print(f'Total Parking: {total_parking}')
        print(f'Occupancy Rate: {occupancy_rate}')
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number"
                ,value = occupancy_rate
                ,title= {'text':'Occupancy Rate'}
                ,gauge={
                    'axis': {'range': [0,100]},
                    'bar': {'color':'darkblue'},
                    'steps': [
                        {'range':[0,50], 'color': 'lightgray'},
                        {'range':[50,100], 'color':'gray'}
                    ],
                    'threshold': {
                        'line': {'color':'red','width':4},
                        'thickness':0.75,
                        'value':80
                    }
                }
            )
        )

        available = total_parking - occupied

        fig2 = go.Figure(
            go.Indicator(
                mode="number+delta"
                ,value = available
                ,title= {'text':'Available Parking'}
                ,delta = {'reference':total_parking, 'relative':True, 'position':'top'}
            )
        )

        sql3 = """
            SELECT
                COUNT(DISTINCT booking_id) AS mtd_booking_count
                ,COUNT(DISTINCT CASE WHEN is_advanced_booking = True AND is_adv_booking_apprv = 2 THEN booking_id END) AS mtd_advanced_booking
                ,EXTRACT(HOUR FROM SUM(end_date::TIME - start_date::TIME)/COUNT(DISTINCT booking_id)) AS avg_booking_hours
                ,EXTRACT(MINUTE FROM SUM(end_date::TIME - start_date::TIME)/COUNT(DISTINCT booking_id)) AS avg_booking_minutes
            FROM booking
            WHERE
            TO_CHAR(booking_date,'YYYY-MM') = TO_CHAR(CURRENT_TIMESTAMP,'YYYY-MM')
        """
        values3 = []
        col3 = ['mtd_booking_count','mtd_advanced_booking','avg_booking_hours','avg_booking_minutes']
        result3 = db.querydatafromdatabase(sql3,values3,col3)
        mtd_booking_count = result3['mtd_booking_count'].iloc[0]
        mtd_advanced_booking_count = result3['mtd_advanced_booking'].iloc[0]
        avg_booking_hours = result3['avg_booking_hours'].iloc[0]
        avg_booking_minutes = result3['avg_booking_minutes'].iloc[0]

        sql4 = """
        SELECT
            TO_CHAR(booking_date,'YYYY-MM') AS booking_month
            ,COUNT(DISTINCT booking_id) AS booking_count
        FROM booking
        WHERE TO_CHAR(booking_date,'YYYY-MM') >= TO_CHAR(DATE_TRUNC('month', CURRENT_TIMESTAMP - INTERVAL '6 month'), 'YYYY-MM')
        GROUP BY
            TO_CHAR(booking_date,'YYYY-MM')
        """
        values4 = []
        cols4 = ['booking_month','booking_count']
        result4 = db.querydatafromdatabase(sql4,values4,cols4)
        
        fig4 = px.bar(result4, x='booking_month', y='booking_count')
        fig4.update_layout(title_text="Monthly Booking Volume")
        return fig, fig2, mtd_booking_count, mtd_advanced_booking_count, f"{int(avg_booking_hours):02d}:{int(avg_booking_minutes):02d}", fig4
    else:
        raise PreventUpdate

