'''
creating an example template for marketing
'''

from urllib.request import urlopen
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

data_path = '/Users/markberreth/Documents/Python_Projects/Comp_Spend'
abbott = pd.read_csv(f'{data_path}/Clean_Data/Abbott_17_18_19_Alt.csv')
location = pd.read_csv(f'{data_path}/Data/ZIP-COUNTY-FIPS_2017-06.csv', dtype={'STCOUNTYFP': str})

abbott = abbott.loc[:, ['Recipient_City', 'Recipient_State', 'Recipient_Zip_Code',
                        'Total_Amount_of_Payment_USDollars', 'Number_of_Payments_Included_in_Total_Amount',
                        'Nature_of_Payment_or_Transfer_of_Value', 'Program_Year', 'Actual_Address',
                        'State', 'Hospital']]

abbott = abbott.merge(location, how='left', left_on='Recipient_Zip_Code', right_on='ZIP')

abbott = abbott.groupby(by=['STCOUNTYFP', 'Program_Year', 'Nature_of_Payment_or_Transfer_of_Value'],
                        as_index=False).sum().reset_index()

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# app layout
app.layout = html.Div([
    html.H1('CMS Competition Spend --- Abbott', style={
        'text-align': 'center'
    }),
    dcc.Dropdown(id='Program_Year',
                 options=[
                     {'label': '2017', 'value': 2017},
                     {'label': '2018', 'value': 2018},
                     {'label': '2019', 'value': 2019}
                 ],
                 multi=False,
                 value=2019,
                 style={'width': '40%'}),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='Comp_Spend', figure={})
])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='Comp_Spend', component_property='figure')],
    [Input(component_id='Program_Year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = f'Year: {option_slctd}'

    dfc = abbott.copy()
    dfc = dfc.loc[dfc['Program_Year'] == option_slctd]
    # you could write another loc function to filter further

    fig = px.choropleth_mapbox(data_frame=dfc,
                               geojson=counties,
                               locations='STCOUNTYFP',
                               color='Total_Amount_of_Payment_USDollars',
                               mapbox_style='carto_darkmatter',
                               labels={'Total_Amount_of_Payment_USDollars': '$ Spent'},
                               zoom=4
                               )

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
