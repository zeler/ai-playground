from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


def classify(features_train, labels_train):

    clf = AdaBoostClassifier(n_estimators=100,
                             learning_rate=1.0)
    clf.fit(features_train, labels_train)

    return clf
