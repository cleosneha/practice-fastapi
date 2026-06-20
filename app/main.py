from fastapi import FastAPI, HTTPException, Query, Path
from service.product import get_all_products, add_product, delete_product, change_product
from schema.product import Product, ProductUpdate
from uuid import uuid4, UUID
from datetime import datetime
app = FastAPI()

@app.get("/")
def root():
    return {"message":"welcome to fastapi"}

# @app.get("/products/{id}")
# def get_product(id: int):
#     products = ['Brush', 'Toothpaste', 'Comb', 'Perfume']

#     if id < 0 or id >= len(products):
#         raise HTTPException(
#             status_code=404,
#             detail="Product not found"
#         )

#     return {"product": products[id]}

@app.get("/get-all-products")
def get_products():
    return get_all_products()



@app.get("/products")
def list_products(name: str = Query(default=None, min_length=1, max_length=50, description="search product by name(case insensitive)"), 
    sort_by_price:bool = Query(default=False, description="sort products by price"),
    order:str = Query(default="asc", description="sort the list in ascending or descending order if sort_by_price is trues"),
    limit:int = Query(default=5,description="show only the number of items passed in limit param", ge=1, le=100),
    offset: int = Query(default=0, ge=0,description="Performing pagination")
    ):
    products = get_all_products()
    
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name","").lower()]
    
    if not products:
        raise HTTPException(status_code=404, detail=f"No product found with this name={name}")

    if sort_by_price:
        # if the order is desc, reverse value will be True
        reverse = order =="desc"
        products = sorted(products, key=lambda p:p.get("price",0), reverse=reverse)
    
    total = len(products)
    products = products[offset:offset+limit]
        
    return {
            "total":total,
            "offset":offset,
            "limit":limit,
            "items": products
    }
    

@app.get("/products/{product_id}")
def get_product_by_id(product_id:int):
    products=get_all_products()
    product = [p for p in products if p["id"] == product_id]
    if not product:
        raise HTTPException(status_code=404,detail=f"product not found with this id={id}")
    return {
        "message" : "product found",
        "product" : product[0]
    }



@app.post("/products",status_code=201)
def create_products(product:Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.now().isoformat() + "Z"
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
            
    return product_dict

@app.delete("/products/{product_id}")
def remove_product(product_id:UUID = Path(...,description="Product ID", example=UUID)):
    try:
        res= delete_product(str(product_id))
        
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/products/{product_id}")
def update_product(product_id:UUID = Path(...,description="Product ID"), payload : ProductUpdate = ...):
    try:
        update_product =  change_product(product_id, payload.model_dump(mode="json", exclude_unset=True))
        return update_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    