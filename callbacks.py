from dash import dcc,html,dash_table,Input,Output,State
import dash_bootstrap_components as dbc
import pandas as pd
import os
import numpy as np
import plotly
import base64, io
from app import app
import plotly.express as px



###################################################################
######################## FUNCIONES ################################
###################################################################


def parse_contents(contents, filename, date):
    #funcion tomada de la documentacion oficial de DASH
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),sep=None,engine='python')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded),sep=None,engine='python')
        elif 'txt' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_csv(io.BytesIO(decoded),sep=None,engine='python')
    except Exception as e:
        print(e)
    return df




#una callback que los lee el documentos del upload

@app.callback(Output("store_link","children"),
              Output("store_file_name","children"),
              Input("link","value"))
def read_link(link):
    if link:
        try:
            df=pd.read_csv(link)
            nam=os.path.basename(link)
            return dcc.Store(id="datos",data=df.to_dict('records')),dcc.Store(id="nombre",data={"nombre":nam})
        except Exception as e:
            print(e)
            return None

#una callback que los lee el documentos del link

@app.callback(Output("store_file","children"),
              Output("store_file_name2","children"),
              Input("id_upload_file","contents"),
              State('id_upload_file', 'filename'),
              State('id_upload_file', 'last_modified'))

def read_file(list_of_contents, list_of_names, list_of_dates):
    #esto recibe listas porque hemos permitido un multiinput, pero realmente, podriamos quitarlo
    #por eso solo estamos seleccionando el primer elemento, si ponemos multiple=False, esto no serian listas
    os.sleep(1)
    df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0]) 
    return dcc.Store(id="datos",data = df.to_dict('records')),dcc.Store(id="nombre",data={"nombre":list_of_names[0]})


#una callback para plotear la tabla una vez que esta en memoria
#@app.callback()


@app.callback(Output("id_upload_type","children"),Input("id_upload_select","value"))

def type_upload(value):

    if value=="Link":
        return dcc.Input(id="link",type="text",placeholder="Introduzca el link (opcional)",style={"width":"100%",'textAlign': 'center','color': 'black'})

    elif value== "Upload file":
        return html.Div([dcc.Upload(id="id_upload_file",children=html.Div(["Arrasta un archivo para cargarlo, \n o buscalo en ",html.B("el ordenador.")]),
                        style={
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '1px'
                                },multiple=True)
                    ])

#radiobutons para seleccionar
@app.callback(Output("id_select_columns","children"),
              Input("datos","data"))
    
def butons(data):
    if len(pd.DataFrame.from_records(data).columns)>3:
        return html.Details(children=[html.Summary('Variables'),dcc.Checklist(pd.DataFrame.from_records(data).columns,pd.DataFrame.from_records(data).columns[:2],
                            id="seleccion",style={'color': 'black'},labelStyle = {'display': 'block'},inputStyle={"margin-right": "20px"})],open=True)
    else:
        return html.Details(children=[html.Summary('Variables'),dcc.Checklist(pd.DataFrame.from_records(data).columns,[],id="seleccion",style={'color': 'black'},
                             labelStyle = {'display': 'block'},inputStyle={"margin-right": "20px"})],open=True)


#para poner la tabla
@app.callback(Output("id_loc_tabla","children"),
              Input("seleccion","value"),
              Input("datos","data"))

def type_upload(selected,data):
    if selected is None:
        return
    else:
        selected1=[{'name': i, 'id': i} for i in selected]
    return dash_table.DataTable(data,columns=selected1,
            page_size=15,style_data={'color': 'black','backgroundColor': '#E6CAC3'},
                                     style_header={'backgroundColor': '#B47A6B'},
                                     filter_action="native",
                                     style_filter={'backgroundColor': '#B47A6B'},
                                     sort_action="native",
                                     sort_mode="multi",
                                     page_action="native",
                                     page_current= 0)


#print name tabla
@app.callback(Output("print_nombre_file","children"),
              Input("nombre","data"))

def print_name(name):
    return html.B(name["nombre"])

#callbacks para los plots
#recibimos los nombres de las variables y damos la opcion de x e y.
@app.callback(Output("id_plot_options","children"),
              Input("datos","data"))

def dropdown(datos):
    nombres_vars=pd.DataFrame.from_records(datos).columns
    nombres_vars_categoricas=pd.DataFrame.from_records(datos).columns[pd.DataFrame.from_records(datos).dtypes!=float]
    return html.Div([html.Hr(),
                     html.Br(),
                     html.Details(children=[html.Summary('Opciones del plot'),
                                            html.Br(),
                                            html.Hr(),
                                            html.B("Eje x"),
                                            dcc.Dropdown(nombres_vars, id='x-dropdown'),
                                            html.B("Eje y"),
                                            dcc.Dropdown(nombres_vars, id='y-dropdown'),
                                            html.B("Color (Variables categoricas o enteras)"),
                                            dcc.Dropdown(nombres_vars_categoricas, id='color'),
                                            html.Br(),
                                            #tipo de graph,
                                            html.H5("Tipo de gráfico"),
                                            dcc.RadioItems(options=[
                                                                {'label': 'Scatter', 'value': 'Scatter'},
                                                                {'label': 'Line', 'value': 'Line'},
                                                                {'label': 'Bar', 'value': 'Bar'},
                                                                {'label': 'Histogram (give only x)', 'value': 'Histogram'}],value="Scatter",
                                                           id="id_type_plot",inline=True,inputStyle={"margin-right": "5px","margin-left": "20px"}),
                                            #escala
                                            html.H5("Escala"),
                                            dcc.Checklist(options=[{'label': 'Escala log en x', 'value': "logx"},
                                                                   {'label': 'Escala log en y', 'value': "logy"}],value=[],
                                                          id="id_log",inline=True,inputStyle={"margin-right": "5px","margin-left": "20px"})
                                            ]
                                )
                    ])

#creamos los plots segun los datos y las x y seleccionados

@app.callback(Output("id_plots","children"),
              Input("y-dropdown","value"),
              Input("x-dropdown","value"),
              State("datos","data"),
              Input("id_type_plot","value"),
              Input("id_log","value"),
              Input("color","value"))

def create_plots(y,x,datos,typ,log,color):
    print(y,x,typ,log,color)
    if "logx" in log:
        log_x=True
    else:
        log_x=False
    if "logy" in log:
        log_y=True
    else:
        log_y=False
    if typ=="Scatter":
        fig = px.scatter(datos, x=x, y=y,color=color,log_x=log_x,log_y=log_y)
    elif typ=="Bar":
        fig = px.bar(datos, x=x, y=y,color=color,log_x=log_x,log_y=log_y)
    elif typ=="Line":
        fig = px.line(datos, x=x, y=y,color=color,log_x=log_x,log_y=log_y)
    elif typ=="Histogram":
        fig = px.histogram(datos, x=x,color=color,log_x=log_x,log_y=log_y)

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(gridcolor="black")
    fig.update_yaxes(gridcolor="black")
    return html.Div([dcc.Graph(figure=fig)])