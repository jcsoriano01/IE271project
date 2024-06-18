# Dash related dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Import the app instance
from app import app

# Importing the layout modules
from apps import commonmodules as cm
from apps import home
from apps import login
from apps import signup
from apps.customers import customers_new as cn
from apps.customers import customers_home as ch
from apps.customers import customers_edit as ce
from apps.customers import customers_approval as ca
from apps.advanced_booking import advanced_booking_new as abn
from apps.advanced_booking import advanced_booking_book as abb
from apps.advanced_booking import advanced_booking_approval as aba
from apps.parking_selection import actual_parking_selection as aps
from apps.parking_selection import actual_parking_selection_book as apsb
from apps.parking_selection import actual_parking_advanced_booking as apab
from apps.customer_information import customer_information_home as cih
from apps.customer_information import customer_information_view as civ
from apps.reports import reports_view as rv

# Styling for content
CONTENT_STYLE = {
    "margin-top": "1em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em"
}

# Defining the layout
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        dcc.Store(id='sessionlogout', data=True, storage_type='session'),
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
        html.Div(cm.navbar, id='navbar_div'),
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

# Callback to handle page navigation and user sessions
@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('navbar_div', 'className'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)
def displaypage(pathname, sessionlogout, userid):
    ctx = dash.callback_context  # Used to determine what triggered the callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'url':
            if userid < 0:
                if pathname in '/':
                    returnlayout = login.layout,
                elif pathname == '/signup':
                    returnlayout = signup.layout,
                else:
                    returnlayout = '404: request not found'
            else:
                if pathname == '/logout':
                    returnlayout = login.layout
                    sessionlogout = True
                elif pathname in ['/','/home']:
                    returnlayout = home.layout
                elif pathname == '/customer_registration':
                    returnlayout = ch.layout,
                elif pathname == '/customer_registration/new':
                    returnlayout = cn.layout,
                elif pathname == '/customer_registration/edit':
                    returnlayout = ce.layout,
                elif pathname == '/customer_registration/for_approval':
                    returnlayout = ca.layout,
                elif pathname == '/advanced_booking/new':
                    returnlayout = abn.layout,
                elif pathname == '/advanced_booking/new/book':
                    returnlayout = abb.layout,
                elif pathname == '/advanced_booking/for_approval':
                    returnlayout = aba.layout,
                elif pathname == '/parking_selection/new':
                    returnlayout = aps.layout,
                elif pathname == '/parking_selection/new/book':
                    returnlayout = apsb.layout,
                elif pathname == '/parking_selection/with_advanced_booking':
                    returnlayout = apab.layout,
                elif pathname == '/customer_information':
                    returnlayout = cih.layout,
                elif pathname == '/customer_information/view/view':
                    returnlayout = civ.layout,
                elif pathname == '/reports':
                    returnlayout = rv.layout,
                else:
                    returnlayout = ['error404'],

            logout_conditions = [
                pathname in ['/','/logout'],
                userid == -1,
                not userid
            ]
            sessionlogout = any(logout_conditions)

            navbar_classname = 'd-none' if sessionlogout else ''
            return [returnlayout, sessionlogout, navbar_classname]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=False)
