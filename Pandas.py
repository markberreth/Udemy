'''
Data Analysis with Pandas and Python
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pokemon = pd.read_csv('/Users/markberreth/PycharmProjects/Udemy/pandas/pokemon.csv')

print(pokemon.describe())

googlestock = pd.read_csv('/Users/markberreth/PycharmProjects/Udemy/pandas/google_stock_price.csv')

print(googlestock.describe())

plt.plot(googlestock)
plt.show()

plt.hist(googlestock['Stock Price'])
plt.show()

print(googlestock.info())
