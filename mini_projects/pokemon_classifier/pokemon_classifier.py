#!/bin/python
import pandas as pd
import matplotlib

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import f_classif, SelectKBest
from sklearn.decomposition import PCA

matplotlib.use('TkAgg')
import seaborn as sns  # noqa

'''
    Simple Pokemon type classifier based on Pokemon stats.
'''


def doPCA(features):
    pca = PCA(n_components=2)
    pca.fit(features)

    print(pca.explained_variance_ratio_)
    print(pca.components_)

df = pd.read_csv('Pokemon.csv')

# data exploration
# drop these columns, no added value
plotdata = df.drop(['Generation', 'Legendary'], 1)

sns.set(color_codes=True)
# sns.jointplot(x="HP", y="Attack", data=plotdata)
# sns.plt.show()

# drop not useful columns and plot stats
plotdata = plotdata.drop(['Total', '#'], 1)

# sns.boxplot(data=plotdata)
# sns.plt.show()

# now include types
plotdata = pd.melt(plotdata,
                   id_vars=["Name", "Type 1", "Type 2"],
                   var_name="Stat")

print(plotdata.head())

sns.set_style("whitegrid")
with sns.color_palette([
    "#8ED752", "#F95643", "#53AFFE", "#C3D221", "#BBBDAF",
    "#AD5CA2", "#F8E64E", "#F0CA42", "#F9AEFE", "#A35449",
    "#FB61B4", "#CDBD72", "#7673DA", "#66EBFF", "#8B76FF",
    "#8E6856", "#C3C1D7", "#75A4F9"],
                        n_colors=18, desat=.9):

    sns.plt.figure(figsize=(12, 10))
    sns.plt.ylim(0, 275)
    sns.swarmplot(x="Stat", y="value", data=plotdata,
                  hue="Type 1", split=True, size=7)
    sns.plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    sns.plt.show()

# there are features with missing data. todo: remove them altogether
df = df.fillna('NA')

# features to use
cols = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed',
        'Type 2']

# Type 1 will be used for labels
labels = df['Type 1'].as_matrix()
features = df[cols].to_dict(orient='records')

# Split training/testing set
train_features, test_features, train_labels, test_labels = train_test_split(
                                             features,
                                             labels,
                                             test_size=0.3,
                                             random_state=42)

# features are in dict format. we need to vectorize them and one-hot
# encode categorized data
feature_vectorizer = DictVectorizer(sparse=False)

# encode labels
label_encoder = LabelEncoder()

# dot actual feature and label transformations
train_features = feature_vectorizer.fit_transform(train_features)
train_labels = label_encoder.fit_transform(train_labels)

test_features = feature_vectorizer.transform(test_features)
test_labels = label_encoder.transform(test_labels)

# do PCA
# doPCA(train_features)

# Feature selector
# selector = SelectKBest(f_classif, k=)
# selector.fit(train_features, train_labels)

# print(selector.scores_)

# train_features = selector.transform(train_features)
# test_features = selector.transform(test_features)

# train model
clf = RandomForestClassifier(n_estimators=50, min_samples_split=5)
clf.fit(train_features, train_labels)

# do prediction for test features
predictions = clf.predict(test_features)

# print accuracy score
print(accuracy_score(test_labels, predictions))
