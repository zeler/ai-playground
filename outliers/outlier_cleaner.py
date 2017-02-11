#!/usr/bin/python
"""
    Clean away the 10% of points that have the largest
    residual errors (difference between the prediction
    and the actual net worth).

    Return a list of tuples named cleaned_data where
    each tuple is of the form (age, net_worth, error).
"""


def outlierCleaner(predictions, ages, net_worths):

    errors = (net_worths - predictions) ** 2
    cleaned_data = zip(ages, net_worths, errors)
    cleaned_data = sorted(cleaned_data, key=lambda x: x[2][0], reverse=True)
    limit = int(len(ages) * 0.1)

    return cleaned_data[limit:]
