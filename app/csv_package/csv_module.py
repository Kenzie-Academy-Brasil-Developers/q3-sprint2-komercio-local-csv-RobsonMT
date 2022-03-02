from csv import DictReader, DictWriter
import os
from flask import Request
import csv

FILEPATH = os.getenv("FILEPATH")
FIELDNAMES = ["id", "name", "price"]

def create_csv_file():
    with open("data/products.csv", "r") as csv_infile:
        csv_products = csv.DictReader(csv_infile, delimiter=",")
        fieldnames = csv_products.fieldnames

        with open(FILEPATH, "w") as csv_outfile:
            writer = DictWriter(csv_outfile, fieldnames)

            writer.writeheader()
            writer.writerows(list(csv_products))


def validate_keys(payload: dict, expected_keys: set):
    body_keys_set = set(payload.keys())
    
    invalid_keys = expected_keys.difference(body_keys_set)

    if invalid_keys:
        raise KeyError(
            {
                "error": "invalid_keys",
                "expected": list(expected_keys),
                "received": list(body_keys_set),
            }
        )


def read_products_in_csv():
    with open(FILEPATH, "r") as csv_file:
        reader = DictReader(csv_file)
        products = list(reader)

    return products


def write_product_in_csv(payload: list[dict]):
    with open(FILEPATH, "a") as infile:
        writer = csv.DictWriter(infile, fieldnames=FIELDNAMES)
        writer.writerow(payload)


def rewrite_product_in_csv(payload: list[dict]):
    with open(FILEPATH, "w") as csv_file:
        writer = DictWriter(csv_file, FIELDNAMES)

        writer.writeheader()
        writer.writerows(payload)


def patch_product_in_csv(body_req: Request, product_id: int) -> dict:
    product_id -=1

    new_name = body_req.get("name")
    new_price = body_req.get("price")

    csv_products = read_products_in_csv()

    if new_name:
        csv_products[product_id].update({"name": new_name})
    if new_price:
        csv_products[product_id].update({"price": new_price})

    new_product = csv_products[product_id]
    new_product.update({"id": int(new_product["id"]),
        "price": float(new_product["price"])
    })

    rewrite_product_in_csv(csv_products)

    return new_product


def paginate_products_in_csv(args, products: list[dict]) -> list:

    page = args.get("page", default=0, type=int)
    per_page = args.get("per_page", default=3, type=int)

    page = int(page)
    per_page = int(per_page)

    start = ((page -1) * per_page)
    end = (page * per_page)

    products_page = list()

    for i, product in enumerate(products):

        if not args:
            if i < per_page:
                products_page.append(product)
        elif i >= start and i < end:
            products_page.append(product)
    
    if not products_page: 
        raise IndexError
       
    return products_page

