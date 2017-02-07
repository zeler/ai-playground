from sklearn.ensemble import RandomForestClassifier


def classify(features_train, labels_train):

    clf = RandomForestClassifier(n_estimators=15, min_samples_split=5)
    clf.fit(features_train, labels_train)

    return clf
