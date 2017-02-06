#!/usr/bin/python
import sys
from time import time
from sklearn import svm
from sklearn.metrics import accuracy_score

sys.path.append("../../../udacity_ud120/tools/")
from email_preprocess import preprocess  # noqa


"""
    THIS CODE REQUIRES PYTHON 2.7

    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:
    Sara has label 0
    Chris has label 1
"""

features_train, features_test, labels_train, labels_test = preprocess(
        words_file="../../../udacity_ud120/tools/word_data.pkl",
        authors_file="../../../udacity_ud120/tools/email_authors.pkl")

# uncomment this to shorten training time
# features_train = features_train[:len(features_train)/100]
# labels_train = labels_train[:len(labels_train)/100]

clf = svm.SVC(kernel="rbf", C=10000)

t0 = time()
clf.fit(features_train, labels_train)
print "training time: ", round(time()-t0, 3), "s"

t0 = time()
predictions = clf.predict(features_test)
print "predicting time: ", round(time()-t0, 3), "s"

# print overall accuracy of this model
print "Accuracy: " + str(accuracy_score(labels_test, predictions))

chrisEmailCnt = 0

for pred in predictions:
    if (pred == 1):
        chrisEmailCnt += 1

print "Chris' emails predicted: " + str(chrisEmailCnt)
