import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import logging

# Application object (stored in app variable), along with CSS stylesheets
app = dash.Dash(__name__, external_stylesheets=["/assets/bootstrap.css"])

# Expose the server attribute for Gunicorn
server = app.server

# Suppress callbacks when input elements enter the layout
app.config.suppress_callback_exceptions = True

# Get CSS from a local folder
app.css.config.serve_locally = True

# Enables your app to run offline
app.scripts.config.serve_locally = True

# Set app title that appears in your browser tab
app.title = 'EZPark'

# The two lines below reduce logs on the terminal to help us debug better
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
