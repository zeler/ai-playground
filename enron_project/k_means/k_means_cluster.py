#!/usr/bin/python
import pickle
import numpy
import matplotlib
import sys
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

sys.path.append("../../udacity_ud120/tools/")
from feature_format import featureFormat, targetFeatureSplit  # noqa

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  # noqa

"""
    This code requires python 2.7
"""


def printMinMaxValue(data):
    minESO = sys.maxint
    maxESO = 0
    minSalary = sys.maxint
    maxSalary = 0

    for person in data:
        if person[2] != 0:
            if person[2] < minESO:
                minESO = person[2]
            if person[2] > maxESO:
                maxESO = person[2]
        if person[1] != 0:
            if person[1] < minSalary:
                minSalary = person[1]
            if person[1] > maxSalary:
                maxSalary = person[1]

    print "Exercised stock options min", minESO, "max", maxESO
    print "Salary min", minSalary, "max", maxSalary

def Draw(pred, features, poi, mark_poi=False, name="image.png",
         f1_name="feature 1", f2_name="feature 2"):

    """ some plotting code designed to help you visualize your clusters """

    # plot each cluster with a different color--add more colors for
    # drawing more than five clusters
    colors = ["b", "c", "k", "m", "g"]
    for ii, pp in enumerate(pred):
        plt.scatter(features[ii][0], features[ii][1], color=colors[pred[ii]])

    # if you like, place red stars over points that are POIs (just for funsies)
    if mark_poi:
        for ii, pp in enumerate(pred):
            if poi[ii]:
                plt.scatter(features[ii][0], features[ii][1],
                            color="r", marker="*")
    plt.xlabel(f1_name)
    plt.ylabel(f2_name)
    plt.savefig(name)
    plt.show()

# load in the dict of dicts containing
# all the data on each person in the dataset
data_dict = pickle.load(open("../../udacity_ud120/final_project/final_project_dataset.pkl", "r"))  # noqa

# there's an outlier--remove it!
data_dict.pop("TOTAL", 0)

# the input features we want to use
# can be any key in the person-level dictionary (salary, director_fees, etc.)
feature_1 = "salary"
feature_2 = "exercised_stock_options"
# feature_3 = "total_payments"
poi = "poi"
features_list = [poi, feature_1, feature_2]
# features_list = [poi, feature_1, feature_2, feature_3]
data = featureFormat(data_dict, features_list)
poi, finance_features = targetFeatureSplit(data)

# min and max for exercised_stock_options
printMinMaxValue(data)

print "After clustering:"

mms = MinMaxScaler()
finance_features = mms.fit_transform(finance_features)

print "Example for salary 200000 and exercised_stock_options 1000000", mms.transform([[200000., 1000000.]])  # noqa

# in the "clustering with 3 features" part of the mini-project,
# you'll want to change this line to
# for f1, f2, _ in finance_features:
# (as it's currently written, the line below assumes 2 features)
for f1, f2 in finance_features:
    plt.scatter(f1, f2)
plt.show()

# cluster here; create predictions of the cluster labels
# for the data and store them to a list called pred

cls = KMeans(n_clusters=2)
pred = cls.fit_predict(data)

# rename the "name" parameter when you change the number of features
# so that the figure gets saved to a different file
try:
    Draw(pred, finance_features, poi, mark_poi=False, name="clusters.pdf",
         f1_name=feature_1, f2_name=feature_2)
except NameError:
    print "no predictions object named pred found, no clusters to plot"
