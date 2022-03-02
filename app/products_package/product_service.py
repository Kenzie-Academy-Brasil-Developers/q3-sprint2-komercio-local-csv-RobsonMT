def validate_id(products: list[dict] ,product_id: int):
    product_with_id = [p for p in products if p["id"] == product_id]

    if not product_with_id:
        raise IndexError
