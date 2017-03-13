import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib

data = pd.read_csv('data.csv', sep='|')
X = data.drop(['Name', 'md5', 'legitimate'], axis=1).values
y = data['legitimate'].values

print('Finding most important feature. Total features %i' % X.shape[1])

clf = ExtraTreesClassifier()
clf.fit(X, y)

model = SelectFromModel(clf, prefit=True)
X_sel = model.transform(X)
nb_features = X_sel.shape[1]

features_train, features_test, labels_train, labels_test = train_test_split(X_sel, y, test_size=0.2)  # noqa

features = []

print('Important features %i' % nb_features)

indices = np.argsort(clf.feature_importances_)[::-1][:nb_features]

for f in range(nb_features):
    print("%d. feature %s (%f)" % (f + 1, data.columns[2 + indices[f]], clf.feature_importances_[indices[f]]))  # noqa

for f in sorted(np.argsort(clf.feature_importances_)[::-1][:nb_features]):
    features.append(data.columns[2+f])

algorithms = {
    "DecisionTree": DecisionTreeClassifier(max_depth=10),
    "RandomForest": RandomForestClassifier(n_estimators=50),
    "GradientBoosting": GradientBoostingClassifier(n_estimators=50),
    "AdaBoost": AdaBoostClassifier(n_estimators=100),
    "GNB": GaussianNB()
}

results = {}

print("Testing algorithms...")

for algo in algorithms:
    clf = algorithms[algo]
    clf.fit(features_train, labels_train)
    score = clf.score(features_test, labels_test)
    print("%s - %f %%" % (algo, score * 100))
    results[algo] = score

winner = max(results, key=results.get)
print("Best algorithm % s with success - %f %%" % (winner, results[winner] * 100))  # noqa

print("Exporting algorithm...")

joblib.dump(algorithms[winner], "classifiers/classifier.pkl")
open("classifiers/features.pkl", "wb").write(pickle.dumps(features))

print("Done")
