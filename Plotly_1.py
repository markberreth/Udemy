import numpy as np
import pandas as pd
import plotly
import plotly.offline as pyo
import plotly.plotly as py
plotly.tools.set_credentials_file(username='markberreth', api_key='N9J13jrusySQD3sHlltl')
import plotly.graph_objs as go
import plotly.dashboard_objs as dashboard

expensedata = pd.read_csv('/Users/markberreth/PycharmProjects/Udemy/Plotly_Data/NumberOfMPsExpenseClaims_2010-2015.csv')

trace0 = go.Scatter(
    x = expensedata['month'],
    y = expensedata['NumberOfClaims2010'],
    mode = 'lines',
    name = 'Claims 2010'
)

trace1 = go.Scatter(
    x = expensedata['month'],
    y = expensedata['NumberOfClaims2011'],
    mode = 'lines',
    name = 'Claims 2011'
)

data0 = [trace0, trace1]

layout = dict(title = 'Claims by Year',
              xaxis = )

fig0 = dict(data = data0, layout = layout)

pyo.plot(fig0, filename='First Line')
url0 = py.plot(fig0, filename='Claims by Year', sharing='secret', auto_open=False)

