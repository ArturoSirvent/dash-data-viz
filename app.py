#importamos lo básico
from dash import Dash
import dash_bootstrap_components as dbc
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets = [dbc.themes.UNITED],url_base_pathname="/page1/",suppress_callback_exceptions=True,
            prevent_initial_callbacks=True) 
            #esto se añade para que no se dispare al empezar, por defecto todas las callbacks se 
            #activan al inicion porque todos los valores se inicializan y cambian lo cual las llama
#eso de supres lo ponemos porque asignamos callbacks a elementos de otras callbacks
server=app.server


if __name__ == '__main__':
    app.run_server(debug=True)

