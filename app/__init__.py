import os
from pickle import TRUE
from xmlrpc.client import Boolean
from flask import Flask ,request , jsonify
from http import HTTPStatus
from pathlib import Path
from app.products_package.product_service import (
 validate_id
)
from app.csv_package.csv_module import (
    create_csv_file,
    patch_product_in_csv,
    read_products_in_csv,
    rewrite_product_in_csv,
    write_product_in_csv,
    paginate_products_in_csv,
    validate_keys,
)

app = Flask(__name__)

FILEPATH = os.getenv('FILEPATH')
csv_file = Path(FILEPATH)

try:
    if not csv_file.is_file(): raise KeyError
except KeyError:
        create_csv_file()

@app.get("/products")
def get_products():

    args = request.args

    products = read_products_in_csv()

    try:
        page = paginate_products_in_csv(args, products)
    except IndexError:
        return {
            "error": f"The current page exceeds the product count limit which is {len(products)}."
        }, HTTPStatus.BAD_REQUEST

    return jsonify(page), HTTPStatus.OK


@app.get('/products/<int:product_id>')
def get_product_by_id(product_id:int):

    products = read_products_in_csv()

    try:
        validate_id(products,product_id)
    except IndexError:
        return {"error": "product id not found"}, HTTPStatus.BAD_REQUEST
    else:
        product = products[(product_id -1)]

        return product, HTTPStatus.OK


@app.post('/products')
def post_product():

    body_req = request.get_json()
    expected_keys = {'name', 'price'}
    products = read_products_in_csv()

    try:
        validate_keys(body_req, expected_keys)
    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST
    else:
        body_req['id'] = (int(products[-1::][0]["id"])+1)

        write_product_in_csv(body_req)

        return body_req, HTTPStatus.CREATED


@app.patch('/products/<int:product_id>')
def patch_product(product_id:int):

    body_req = request.get_json()
    expected_keys = {'name', 'price'}
    products = read_products_in_csv()

    try:
        validate_id(products,product_id)
        validate_keys(body_req, expected_keys)
        updated_product = patch_product_in_csv(body_req, product_id)
    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST
    except IndexError:
        return {"error": "product id not found"}, HTTPStatus.BAD_REQUEST
    else:
        return jsonify(updated_product), HTTPStatus.OK


@app.delete('/products/<product_id>')
def delete_product(product_id):

    products = read_products_in_csv()
   
    try:
        validate_id(products,product_id)
    except IndexError:
        return {"error": "product id not found"}, HTTPStatus.BAD_REQUEST
    else:
        new_list = [p for p in products if p["id"] != product_id]

        rewrite_product_in_csv(new_list)

        product = [p for p in products if p["id"] == product_id][0]
        product.update(
            {"id": int(product['id']), "price": float(product['price'])}
        )

        return product, HTTPStatus.OK

