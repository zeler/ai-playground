#!/bin/python
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

'''
    Simple Pokemon type classifier based on Pokemon stats.

    TODO: maybe change algorithm, use less features...
'''

df = pd.read_csv('Pokemon.csv')

# there are features with missing data. todo: remove them altogether
df = df.fillna('NA')

# features to use
cols = ['Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed',
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

# train model
clf = RandomForestClassifier(n_estimators=50, min_samples_split=5)
clf.fit(train_features, train_labels)

# do prediction for test features
predictions = clf.predict(feature_vectorizer.transform(test_features))

# print accuracy score
print(accuracy_score(label_encoder.transform(test_labels), predictions))
