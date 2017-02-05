from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score


def NBAccuracy(features_train, labels_train, features_test, labels_test):

    clf = GaussianNB()
    clf.fit(features_train, labels_train)

    prediction = clf.predict(features_test)
    accuracy = accuracy_score(labels_test, prediction)

    return accuracy
