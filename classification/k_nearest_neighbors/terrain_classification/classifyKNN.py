from sklearn.neighbors import KNeighborsClassifier


def classify(features_train, labels_train):

    clf = KNeighborsClassifier(algorithm='auto',
                               n_neighbors=3,
                               weights='distance')
    clf.fit(features_train, labels_train)

    return clf
