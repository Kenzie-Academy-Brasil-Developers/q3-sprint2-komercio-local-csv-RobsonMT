from flask import Flask ,request , jsonify
from http import HTTPStatus
import os
from app.products_package.product_service import (
    update_id_of_products, validate_id
)
from app.csv_package.csv_module import (
    patch_product_in_csv,
    read_products_from_csv,
    rewrite_product_in_csv,
    write_product_in_csv,
    paginate_products_in_csv,
    find_product_by_id,
    validate_keys,
)

app = Flask(__name__)

@app.get("/products")
def get_products():

    args = request.args

    products = paginate_products_in_csv(args)

    return jsonify(products), HTTPStatus.OK


@app.get('/products/<int:product_id>')
def get_product_by_id(product_id:int):

    products = read_products_from_csv()

    try:
        validate_id(products,product_id)
    except IndexError:
        return {"error": "product id not found"}, HTTPStatus.BAD_REQUEST
    else:
        product = find_product_by_id(product_id)
        return product, HTTPStatus.OK


@app.post('/products')
def post_product():

    body_req = request.get_json()
    products = read_products_from_csv()
    expected_keys = {'name', 'price'}

    try:
        validate_keys(body_req, expected_keys)
    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST

    body_req['id'] = len(list(products))+1

    write_product_in_csv(body_req)

    return body_req, HTTPStatus.CREATED


@app.patch('/products/<int:product_id>')
def patch_product(product_id:int):

    body_req = request.get_json()

    try:
        updated_product = patch_product_in_csv(body_req, product_id)
    except IndexError:
        return {"error": "product id not found"}, HTTPStatus.BAD_REQUEST
    else:
        return updated_product, HTTPStatus.OK


@app.delete('/products/<product_id>')
def delete_product(product_id):

    products = read_products_from_csv()

    try:
        validate_id(products,product_id)
    except IndexError:
        return {
            "error": "product id not found"
        }, HTTPStatus.BAD_REQUEST
    else:
        new_products = update_id_of_products(
            [p for p in products if p["id"] != product_id]
        )
        rewrite_product_in_csv(new_products)
        return {}, HTTPStatus.OK

