#!/bin/python
import pandas


def simple_heuristic(df):

    predictions = {}

    for passenger_index, passenger in df.iterrows():
        passenger_id = passenger['PassengerId']

        if (passenger['Sex'] == 'female' or
                (passenger['Pclass'] == 1 and
                    passenger['Age'] < 18) or
                (passenger['Pclass'] == 2 and
                    passenger['Age'] < 18 and
                    passenger['Parch'] > 0)):

            predictions[passenger_id] = 1
        else:
            predictions[passenger_id] = 0

    return predictions


if __name__ == '__main__':

    df = pandas.read_csv('titanic_data.csv')
    predictions = simple_heuristic(df)
    count = 0

    for passenger_index, passenger in df.iterrows():
        passenger_id = passenger['PassengerId']

        if passenger['Survived'] == predictions[passenger_id]:
            count += 1

    print(count / float(len(df.index)))
