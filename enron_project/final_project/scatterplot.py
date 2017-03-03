#!/bin/python
import sys
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  # noqa

sys.path.append("../../udacity_ud120/tools/")
from feature_format import featureFormat, targetFeatureSplit  # noqa


def show_scatterplot(data_dict, features):
    data = featureFormat(data_dict, features)

    for point in data:
        plt.scatter(point[0], point[1])

    plt.xlabel(features[0])
    plt.ylabel(features[1])
    plt.show()
