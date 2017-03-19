#!/bin/python
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor

matplotlib.use('TkAgg')
import seaborn as sns  # noqa


# load data
df = pd.read_csv('data.csv')

# print first n rows
print(df.head())

X = df['Hours'].values[:, np.newaxis]
y = df['Score'].values

# create and fit linear_model
reg = SGDRegressor(learning_rate="invscaling")
reg.fit(X, y)

print("Slope:", reg.coef_, "Intercept:", reg.intercept_)
print("Predicted score for 55 hours:", reg.predict(55))
print("R-squared:", reg.score(X, y))

# display data in jointplot
plt.scatter(X, y, color='g')
plt.plot(X, reg.predict(X), color='k')

plt.show()
