import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

server = app.server

apple = pd.read_csv('')

app.layout = html.Div(children=[
    html.H1('Apple Stock Price'),
    html.Div('Dash: Dashboard with Python'),
    dcc.Graph(id='apple',
              figure={'data': apple,
                      'layout': {
                          'title':'Apple Stock Price'
                                 }
                      }
              )
])

if __name__ == '__main__':
    app.run_server()
