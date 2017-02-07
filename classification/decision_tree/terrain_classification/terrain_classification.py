#!/usr/bin/python
import sys
from classifyDT import classify
from sklearn.metrics import accuracy_score

sys.path.append("../../common")
from class_vis import prettyPicture, output_image  # noqa
from prep_terrain_data import makeTerrainData  # noqa

""" lecture and example code for decision tree unit """

features_train, labels_train, features_test, labels_test = makeTerrainData()

clf = classify(features_train, labels_train)
prettyPicture(clf, features_test, labels_test)

pred = clf.predict(features_test)
print("Accuracy: " + str(accuracy_score(labels_test, pred)))
