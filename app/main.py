from fastapi import FastAPI, HTTPException, Query
from service.product import get_all_products
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
    limit:int = Query(default=5,description="show only the number of items passed in limit param", ge=1, le=100)
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
    products = products[0:limit]
        
    return {
            "total":total,
            "limit":limit,
            "items": products
    }
    
    