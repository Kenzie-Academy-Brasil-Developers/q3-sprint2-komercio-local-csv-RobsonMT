def update_id_of_products(payload: list[dict]) -> list[dict]:
    for i, _ in enumerate(payload, 1):
        payload[(i-1)].update({'id': i})
    return payload
    

def validate_id(products: list[dict] ,product_id: int) :
    if (int(product_id) > (len(products))):
        raise IndexError
   
    