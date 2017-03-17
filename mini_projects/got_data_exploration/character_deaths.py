#!/bin/python
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder
import matplotlib

matplotlib.use('TkAgg')
import seaborn as sns  # noqa

df = pd.read_csv('game-of-thrones/character-deaths.csv')

counter_nan = df.isnull().sum()
print("Data with NaN: \n%s" % (counter_nan))

counter_without_nan = counter_nan[counter_nan == 0]
print("Data without NaN: \n%s" % (counter_without_nan))

df = df[counter_without_nan.keys()]

X = df.ix[:, 1:]

le = LabelEncoder()
X['Allegiances'] = le.fit_transform(X['Allegiances'])
print(X.head())

tsne = TSNE(n_components=2, random_state=42)
X_test_2d = pd.DataFrame(tsne.fit_transform(X))

sns.jointplot(x="Gender", y="Nobility", data=df)
sns.plt.show()

sns.jointplot(x=0, y=1, data=X_test_2d)
sns.plt.show()

