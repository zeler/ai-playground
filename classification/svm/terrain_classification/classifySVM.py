from sklearn.svm import SVC


def classify(features_train, labels_train):

    clf = SVC(kernel="linear")
    clf.fit(features_train, labels_train)

    return clf
