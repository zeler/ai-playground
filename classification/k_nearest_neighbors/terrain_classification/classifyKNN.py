from sklearn.neighbors import KNeighborsClassifier


def classify(features_train, labels_train):

    clf = KNeighborsClassifier(algorithm='ball_tree',
                               n_neighbors=11,
                               weights='distance')
    clf.fit(features_train, labels_train)

    return clf
