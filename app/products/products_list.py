from flask import jsonify
import csv
import os

def products_list():
    products = []

    FILEPATH = os.getenv('FILEPATH')

    with open(FILEPATH, 'r') as products_list_csv:
        csv_dict_reader = csv.DictReader(products_list_csv, delimiter=",")

        for line in csv_dict_reader:
            products.append(line)

    # f = open(FILEPATH, "r")

    # reader = csv.DictReader(f)

    # for line in reader:
    #     products.append(line)

    # f.close()
    
    return products