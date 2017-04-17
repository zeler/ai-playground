#!/bin/python
import pandas as pd
from pandas import DataFrame
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


if __name__ == '__main__':

    df = pd.read_csv('titanic_data.csv')
    df = df.drop(['PassengerId', 'Name', 'Ticket', 'Fare', 'Cabin'], 1)

    df['Sex'] = pd.factorize(df['Sex'])[0]
    df['Embarked'] = pd.factorize(df['Embarked'])[0]

    df = df.dropna()

    clf = DecisionTreeClassifier()
    clf.fit(df.ix[:, df.columns != 'Survived'], df['Survived'])

    print(accuracy_score(df['Survived'], clf.predict(df.ix[:, df.columns != 'Survived'])))
