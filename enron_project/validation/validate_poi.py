#!/usr/bin/python

"""
    This code requires python 2.7

    Starter code for the validation mini-project.
    The first step toward building your POI identifier!

    Start by loading/formatting the data

    After that, it's not our code anymore--it's yours!
"""

import pickle
import sys
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split

sys.path.append("../../udacity_ud120/tools/")
from feature_format import featureFormat, targetFeatureSplit  # noqa

data_dict = pickle.load(open("../../udacity_ud120/final_project/final_project_dataset.pkl", "r"))  # noqa

# first element is our labels, any added elements are predictor
# features. Keep this the same for the mini-project, but you'll
# have a different feature list when you do the final project.
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

train_features, test_features, train_labels, test_labels = train_test_split(
    features, labels, test_size=0.3, random_state=42)

clf = DecisionTreeClassifier()
clf.fit(train_features, train_labels)

print "Accuracy:", accuracy_score(test_labels, clf.predict(test_features))

