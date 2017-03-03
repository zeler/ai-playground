#!/usr/bin/python

"""
    This code requires Python 2.7

    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

sys.path.append("../../udacity_ud120/tools/")
from feature_format import featureFormat, targetFeatureSplit  # noqa

data_dict = pickle.load(open("../../udacity_ud120/final_project/final_project_dataset.pkl", "r"))  # noqa

# add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

# your code goes here 
train_features, test_features, train_labels, test_labels = train_test_split(
    features, labels, test_size=0.3, random_state=42)

clf = DecisionTreeClassifier()
clf.fit(train_features, train_labels)

pois = clf.predict(test_features)

cnt = 0
for poi in pois:
    if poi == 1.0:
        cnt += 1

print "Test set size:", len(pois)
print "Test POI count:", cnt

cnt = 0
for idx, poi in enumerate(pois):
    if poi == 1.0 and test_labels[idx] == 1.0:
        cnt += 1

print "True positives:", cnt

print "Precision score:", precision_score(test_labels, pois)
print "Recall score:", recall_score(test_labels, pois)
