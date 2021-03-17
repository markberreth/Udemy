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
px.set_mapbox_access_token(
    'pk.eyJ1IjoibWFya2JlcnJldGgiLCJhIjoiY2ttY3VzOHhtMGVmaDJvbGppMW9jZWRudyJ9.mdmXPjveC_oXO8CHeyxytQ')

data_path = '/Users/markberreth/Documents/Python_Projects/Comp_Spend'
abbott = pd.read_csv(f'{data_path}/Clean_Data/Abbott_17_18_19_Alt.csv')
location = pd.read_csv(f'{data_path}/Data/ZIP-COUNTY-FIPS_2017-06.csv', dtype={'STCOUNTYFP': str})

columns = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 'feature class',
           'feature code', 'country code', 'cc2', 'admin1 code', 'admin2 code', 'admin3 code',
           'admin4 code', 'population', 'elevation', 'dem', 'timezone', 'modification date']
ref_data = pd.read_csv(f'{data_path}/Data/US.txt', sep='\t', header=0)
ref_data.columns = columns
ref_data.drop(columns=['asciiname', 'alternatenames', 'feature class', 'feature code', 'country code',
                       'cc2', 'population', 'elevation', 'dem', 'timezone', 'modification date'],
              inplace=True)
ref_data['name'] = ref_data['name'].str.upper()

abbott['Recipient_City'] = abbott['Recipient_City'].str.upper()
abbott = abbott.loc[:, ['Recipient_City', 'Recipient_State', 'Recipient_Zip_Code',
                        'Total_Amount_of_Payment_USDollars', 'Number_of_Payments_Included_in_Total_Amount',
                        'Nature_of_Payment_or_Transfer_of_Value', 'Program_Year', 'Actual_Address',
                        'State', 'Hospital']]

abbott = abbott.groupby(by=['Recipient_City', 'Recipient_State', 'Program_Year'],
                        as_index=False).sum().reset_index()

abbott = abbott.merge(ref_data, how='left', left_on=['Recipient_City', 'Recipient_State'],
                      right_on=['name', 'admin1 code'])
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)

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

    fig = px.scatter_mapbox(dfc, lat='latitude',
                            lon='longitude',
                            color='Number_of_Payments_Included_in_Total_Amount',
                            hover_data=['Recipient_City',
                                        'Total_Amount_of_Payment_USDollars'],
                            size='Total_Amount_of_Payment_USDollars',
                            mapbox_style='carto_darkmatter',
                            size_max=20,
                            labels={'Number_of_Payments_Included_in_Total_Amount': 'Total # Payments',
                                    'Total_Amount_of_Payment_USDollars': '$ Total'}
                            )
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
