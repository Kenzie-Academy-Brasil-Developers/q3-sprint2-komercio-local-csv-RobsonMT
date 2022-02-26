from csv import DictReader, DictWriter
from http import HTTPStatus
from flask import Request
import csv

FILEPATH = "app/products/products.csv"
FIELDNAMES = ['id', 'name', 'price']


def validate_keys(payload: dict, expected_keys: set):
    body_keys_set = set(payload.keys())

    invalid_keys = body_keys_set.difference(expected_keys)

    if invalid_keys:
        raise KeyError(
            {
                "error": "invalid_keys",
                "expected": list(expected_keys),
                "received": list(body_keys_set),
            }
        )


def read_products_from_csv():
    with open(FILEPATH, "r") as csv_file:
        reader = DictReader(csv_file)
        products = list(reader)

    return products


def write_product_in_csv(payload: list[dict]):
    with open(FILEPATH, 'a') as infile:
        writer = csv.DictWriter(infile, fieldnames=FIELDNAMES)
        writer.writerow(payload)


def rewrite_product_in_csv(payload: list[dict]):
    with open(FILEPATH, "w") as csv_file:
        writer = DictWriter(csv_file, FIELDNAMES)

        writer.writeheader()
        writer.writerows(payload)


def patch_product_in_csv(body_req: Request, product_id: int) -> dict:
    product_id -=1

    new_name = body_req.get('name')
    new_price = body_req.get('price')

    csv_products = read_products_from_csv()

    if new_name:
        csv_products[product_id].update({'name': new_name})
    if new_price:
        csv_products[product_id].update({'price': new_price})

    new_product = csv_products[product_id]

    rewrite_product_in_csv(csv_products)

    return new_product


def paginate_products_in_csv(args) -> list:

    page = args.get('page')
    per_page = args.get('per_page')

    if not page: page = 0
    if not per_page: per_page = 3
    
    products_page = list()

    products = read_products_from_csv()
  
    for i, product in enumerate(products):

        start = ((int(page) -1) * int(per_page))
        end = (int(page) * int(per_page))

        if not page and per_page:
            if i < per_page:
                products_page.append(product)

        elif i >= start and i < end:
            products_page.append(product)

    return products_page


def find_product_by_id(product_id:int) -> dict:

    products = read_products_from_csv()
    product = dict()

    for curr_product in products:
        if int(curr_product['id']) == product_id:
            product = curr_product
    
    return product
