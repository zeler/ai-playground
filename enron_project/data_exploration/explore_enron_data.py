#!/usr/bin/python
import pickle

"""
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
"""
enron_data = pickle.load(
    open("../../udacity_ud120/final_project/final_project_dataset.pkl", "rb"))

print("Total persons:", len(enron_data))
print("Features:", len(enron_data["SKILLING JEFFREY K"]))

cnt = 0
max_total_payment = 0
max_total_payment_poi = ""
salary_cnt = 0
email_address_cnt = 0
unknown_total_payments = 0
unknown_poi_total_payments = 0

for person in enron_data:
    if enron_data[person]["poi"] == 1:
        cnt += 1
        if max_total_payment < enron_data[person]["total_payments"]:
            max_total_payment = enron_data[person]["total_payments"]
            max_total_payment_poi = person
    if enron_data[person]["salary"] != "NaN":
        salary_cnt += 1
    if enron_data[person]["email_address"] != "NaN":
        email_address_cnt += 1
    if enron_data[person]["total_payments"] == "NaN":
        unknown_total_payments += 1
        if enron_data[person]["poi"] == 1:
            unknown_poi_total_payments += 1

print("Actual data for POI:", cnt)
print("Features:", enron_data["PRENTICE JAMES"].keys())

print("\nSample data:\n")

print("JAMES PRENTICE stock value:", enron_data["PRENTICE JAMES"]
                                               ["total_stock_value"])
print("COLWELL WESLEY email count:", enron_data["COLWELL WESLEY"]
                                               ["from_this_person_to_poi"])
print("SKILLING JEFFREY K exercised stock options:",
      enron_data["SKILLING JEFFREY K"]["exercised_stock_options"])
print("POI with max total payments:", max_total_payment_poi, "-",
      max_total_payment)
print("Salary information:", salary_cnt)
print("Known email addresses:", email_address_cnt)
print("Unknown total payments:", unknown_total_payments, "which is",
      unknown_total_payments / len(enron_data) * 100, "% of all persons")
print("Unknown total payments for POI:", unknown_poi_total_payments, "which is",
      unknown_poi_total_payments / cnt * 100, "% of all POIs")

print("\nPersons of interest:\n")

cnt = 0
with open('../../udacity_ud120/final_project/poi_names.txt', 'r') as f:
    for line in f:
        if (line.startswith("(")):
            cnt += 1
            print(line, end='')

print("\nPOI total count:", cnt)