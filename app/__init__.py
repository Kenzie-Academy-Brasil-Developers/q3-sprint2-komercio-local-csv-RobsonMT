from multiprocessing.sharedctypes import Value
from flask import Flask ,request , jsonify
from http import HTTPStatus
import csv
import os

app = Flask(__name__)

FILEPATH = os.getenv('FILEPATH')

@app.get('/products')
def get_products_with_query_parameters():

    args = request.args
    page = args.get('page')
    per_page = args.get('per_page')

    if not page:
        page = 0
    
    if not per_page:
        per_page = 3

    products = list()

    with open(FILEPATH, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=",")

        for i, product in enumerate(reader):

            if not args:
                if i < per_page:
                    products.append(product)

            elif i >= ((int(page) -1) * int(per_page)) and i < (int(page) * int(per_page)):
                products.append(product)

    return jsonify(products), HTTPStatus.OK


@app.get('/products/<int:product_id>')
def get_product_id(product_id):

    product = dict()

    with open(FILEPATH, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=",")

        for curr_product in reader:
            if int(curr_product['id']) == product_id:
                product = curr_product

    return jsonify(product), HTTPStatus.OK


@app.post('/products')
def post_product():

    req = request.get_json()

    with open(FILEPATH, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=",")

        req['id'] = len(list(reader))+1

    fieldnames = reader.fieldnames

    payload = req

    with open(FILEPATH, 'a', encoding='utf-8') as infile:
    
        writer = csv.DictWriter(infile, fieldnames=fieldnames)

        writer.writerow(payload)

    return payload, HTTPStatus.CREATED


@app.patch('/products/<int:product_id>')
def patch_product_id(product_id):

    req = request.get_json()
    new_name = req.get('name')
    new_price = req.get('price')

    expected_keys = {'name', 'price'}
    received_keys = set(req.keys())

    new_list_csv = list()
    new_product = {}

    with open(FILEPATH, encoding='utf-8') as infile:

        table = csv.DictReader(infile, delimiter=',')

        tb_header = table.fieldnames

        for i, row in enumerate(table):
            if i == 0:
                new_list_csv.append(tb_header)
                
            elif int(row['id']) == product_id:
                if new_price:
                    row.update({'price': new_price})
                if new_name:
                    row.update({'name': new_name})

            new_list_csv.append(row.values())

    outfile = open(FILEPATH, 'w', newline='', encoding='utf-8')

    write = csv.writer(outfile)

    for i, row in enumerate(new_list_csv):
        write.writerow(row)

    outfile.close() 

    new_product = {
        'id': product_id, 'name': new_name, 'price': new_price
    }

    invalid_keys = received_keys.difference(expected_keys)

    if invalid_keys:
        return {
            "error": "invalid_keys",
            "expected": list(expected_keys),
            "received": list(received_keys)
        }, HTTPStatus.BAD_REQUEST
  
    if product_id >= len(new_list_csv):
        return {"error": "product id 1 not found"}, HTTPStatus.BAD_REQUEST
    
    return new_product, HTTPStatus.OK

@app.delete('/products/<int:product_id>')
def delete_product_id(product_id):

    new_list_csv = list()

    with open(FILEPATH, encoding='utf-8') as infile:

        table = csv.reader(infile, delimiter=',')

        tb_header = next(table)

        new_list_csv.append(tb_header)

        for row in table:
            new_list_csv.append(row)

    removed_product = new_list_csv.pop(product_id)

    if product_id >= len(new_list_csv):
        return {"error": "product id 1 not found"}, HTTPStatus.BAD_REQUEST

    outfile = open(FILEPATH, 'w', newline='', encoding='utf-8')

    write = csv.writer(outfile)

    for row in new_list_csv:
        write.writerow(row)

    outfile.close() 

    return dict(removed_product), HTTPStatus.OK
        

   
