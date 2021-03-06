#!/usr/bin/python
import sys
import numpy
import matplotlib
import matplotlib.pyplot as plt
from linearReg import linearReg

sys.path.append("../../common")
from class_vis import plot_regression  # noqa
from ages_net_worths import ageNetWorthData  # noqa

matplotlib.use('agg')

ages_train, ages_test, net_worths_train, net_worths_test = ageNetWorthData()
reg = linearReg(ages_train, net_worths_train)

plot_regression(reg, ages_train, ages_test, net_worths_train, net_worths_test)

print("Net worth prediction:", reg.predict([[29]])[0][0])
print("Slope", reg.coef_[0][0])
print("Intercept", reg.intercept_[0])

print("Test r-squared:", reg.score(ages_test, net_worths_test))
print("Train r-squared:", reg.score(ages_train, net_worths_train))
