#!/bin/python
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score

'''
    Simple Pokemon type classifier based on Pokemon stats.BaseException

    TODO: maybe change algorithm, use less features...
'''

df = pd.read_csv('Pokemon.csv')
df = df.fillna('NA')

cols = ['Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed',
        'Type 2']

labels = df['Type 1'].as_matrix()
features = df[cols].to_dict(orient='records')

train_features, test_features, train_labels, test_labels = train_test_split(
                                             features,
                                             labels,
                                             test_size=0.3,
                                             random_state=42)

feature_vectorizer = DV(sparse=False)
label_encoder = LabelEncoder()

train_features = feature_vectorizer.fit_transform(train_features)
train_labels = label_encoder.fit_transform(train_labels)

clf = RandomForestClassifier(n_estimators=50, min_samples_split=5)
clf.fit(train_features, train_labels)
predictions = clf.predict(feature_vectorizer.transform(test_features))

print(test_labels)
print(label_encoder.inverse_transform(predictions))
print(accuracy_score(label_encoder.transform(test_labels), predictions))
