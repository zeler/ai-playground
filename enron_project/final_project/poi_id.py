#!/usr/bin/python

import sys
import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split
from tester import dump_classifier_and_data
from dataset_info import print_dataset_info
from scatterplot import show_scatterplot

sys.path.append("../../udacity_ud120/tools/")
from feature_format import featureFormat, targetFeatureSplit  # noqa


# Task 1: Select what features you'll use.
# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".
features_list = ['poi', 'salary', 'bonus', 'exercised_stock_options', 'total_stock_value', 'from_this_person_to_poi', 'from_poi_to_this_person']  # noqa

# Load the dictionary containing the dataset
with open("../../udacity_ud120/final_project/final_project_dataset.pkl", "r") as data_file:  # noqa
    data_dict = pickle.load(data_file)

print_dataset_info(data_dict)
# Task 2: Remove outliers
data_dict.pop("TOTAL", 0)

# Task 3: Create new feature(s)
# Store to my_dataset for easy export below.
my_dataset = data_dict

# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

# Task 4: Try a varity of classifiers
# Please name your classifier clf for easy export below.
# Note that if you want to do PCA or other multi-stage operations,
# you'll need to use Pipelines. For more info:
# http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
clf = GaussianNB()

# Task 5: Tune your classifier to achieve better than .3 precision and recall
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info: 
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)
