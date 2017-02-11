#!/usr/bin/python
import pickle
import sys
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  # noqa

sys.path.append("../../udacity_ud120/tools/")
from feature_format import featureFormat, targetFeatureSplit  # noqa


"""
    THIS CODE REQUIRE PYTHON 2.7
"""

# read in data dictionary, convert to numpy array
data_dict = pickle.load(open("../../udacity_ud120/final_project/final_project_dataset.pkl", "r"))  # noqa
features = ["salary", "bonus"]
data_dict.pop("TOTAL", 0)
data = featureFormat(data_dict, features)

for point in data:
    salary = point[0]
    bonus = point[1]
    plt.scatter(salary, bonus)

plt.xlabel("salary")
plt.ylabel("bonus")
plt.show()
