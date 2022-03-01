7############################################################################
########################## ENUNCIADO EJERCICIO EN DASH #####################
# DataSet Viewer: Crear un proyecto dash para explorar datasets (csv’s)
# mediante su visualización (layout similar al ejemplo de
# complex interaction.py .
#   • Carga del data set (upload desde el disco, opcional url)
#   • Selección de las columnas a visualizar (opcional selección de
# escala: log/lineal) (dropdown, radio-buttons,..)
#   • Selección del tipo de gráfico (radio-buttons, check-boxes,...): line,
# scatter, dist, ... (añadir tantos tipos como veáis conveniente,
# cuantos más mejor)
#   • Gráfico: Visualización del gráfico principal
#   • Opcional-1: Incluir varios gráficos en una página
#   • Opcional-2: Incluir varios gráficos (multi-página)
############################################################################

from dash import dcc,html,Input,Output, dependencies,State
#importamos el objeto app
from app import app
import callbacks


#importamos los layouts ya prefabricados (por mi) en funciones y variables en otro archivo
from layouts import * 

#importamos las funciones tambien


#construimos el esqueleto que se llenará con los modulos de Layouts

app.layout=dbc.Container([
    dcc.Location(id="url",refresh=True),
    html.Div(id="page-content",)
],fluid=True)# ,style={"backgroundColor":"#f7f0dc"}


#creamos la callback que actua para actualizar las paginas 


@app.callback(Output("page-content","children"),
              Input("url","pathname"))
def display_page(pathname):
    print(pathname)
    if pathname == '/page1/':
         return page1
    #elif pathname == '/page2/':
    #    return page2
    else:
        return '404' 

if __name__ == '__main__':
    app.run_server(debug=True)