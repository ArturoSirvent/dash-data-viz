from dash import dcc, html,dash_table
import dash as dbc
import dash_bootstrap_components as dbc
from matplotlib import style
#import pandas as pd
#import numpy as np




colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}



page1 = html.Div([
    dbc.Row([
        #creamos una columna lateral en gris para meter las opciones
        dbc.Col(
            html.Div([
                #Añadimos un titulo de encabezado
                html.H1("Visualización interactiva de datos",style={"text-align":"center",'color': 'black'}),
                dcc.Dropdown(options=["Link","Upload file"],id="id_upload_select"),
                html.Div(id="id_upload_type"),
                html.Div([html.Div(id="store_link"),html.Div(id="store_file"),html.Div(id="store_file_name"),html.Div(id="store_file_name2")]),
                html.Div(id="id_select_columns"),
                html.Div(id="id_plot_options")
            
            ],style={'borderBottom': 'thin lightgrey solid',
                     'padding': '10px 10px'}),width={"size": 3, "offset": 0},style={"backgroundColor":"#f2dda2"}),
        dbc.Col(
            dbc.Row([
                html.Div([
                    html.H1("Visualizado",style={"text-align":"center",'color': 'black'}),
                    html.Div(id="print_nombre_file"),
                    html.Div(id="id_loc_tabla")
                ]),
            dbc.Row([
                html.Div(id="id_plots")
            ])
            ]),style={"backgroundColor":"#f7f0dc"})
    ])
])

