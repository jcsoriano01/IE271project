from dash import dcc
from dash import html
import dash_html_components as dhtml
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate

#import app object
from app import app

#CSS Styling for the NavLink components
navlink_style = {
    'color': '#f0f0f0',
    #'color': '#88D317',
    'margin': '0 10px',
    'font-family': 'Georgia',
}

dropdown_menu_style = {
    'font-family':'Georgia',
}

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # dbc.Row(
                #     [
                #         dbc.Col(dbc.NavbarBrand("EZPark", className="ms-2")),
                #     ],
                #     align='center',
                #     className='g-0',  # remove gutters (horizontal space between cols)
                # ),
                #dbc.NavbarBrand("EZPark", className="ms-2")
                "EZPark"
                ,className='navbar-brand'
                ,href='/home',
            ),
            dbc.Button(
                    dhtml.Span(className='navbar-toggler-icon')
                    , type = 'button'
                    , className = 'navbar-toggler'
                    #, **{'data-bs-toggle': 'collapse', 'data-bs-target': '#navbarSupportedContent'}
            )
            ,
            dbc.Nav(
                [
                    dbc.DropdownMenu(
                            label = 'Customer Registration',
                            nav = True,
                            in_navbar = True,
                            children  = [
                                dbc.DropdownMenuItem("New", href = '/customer_registration/new'),
                                dbc.DropdownMenuItem("Edit", href = '/customer_registration/edit'),
                                dbc.DropdownMenuItem("For Approval", href='/customer_registration/for_approval'),
                            ],
                            toggle_style = {'cursor':'pointer'},
                            style=navlink_style
                    ),
                    dbc.DropdownMenu(
                            label = 'Advance Booking',
                            nav = True,
                            in_navbar = True,
                            children = [
                                dbc.DropdownMenuItem("New", href='/advanced_booking/new', style = dropdown_menu_style),
                                dbc.DropdownMenuItem("For Approval", href='/advanced_booking/for_approval', style = dropdown_menu_style),
                            ]
                    ),
                    dbc.DropdownMenu(
                            label = 'Parking Selection',
                            nav = True,
                            in_navbar = True,
                            children  = [
                                dbc.DropdownMenuItem("New", href = '/parking_selection/new'),
                                dbc.DropdownMenuItem("With Advance Booking", href = '/parking_selection/with_advanced_booking'),
                            ],
                            toggle_style = {'cursor':'pointer'},
                            style=navlink_style
                    ),
                    dbc.NavLink("Customer Information", href='/customer_information', style=navlink_style),
                    dbc.NavLink("Reports", href='/reports', style=navlink_style),
                    dbc.NavLink("Logout", href='/logout', style=navlink_style),
                    
                ],
                className="ms-auto",
                navbar=True
            )
        ],
        fluid=True
    ),
    dark=True,
    #color='#616161',
    #color = '#008080', #--teal
    #color = '#1A0315', #darkplum
    #color = '#6E3667',
    #color = '#778899', #grey
    color = '#2F4F4F',
    expand='lg'
)
