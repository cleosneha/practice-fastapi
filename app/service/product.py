import json
from pathlib import Path
from typing import List, Dict
from fastapi import HTTPException

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "dummy.json"

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        raise HTTPException(status_code=404, detail="No product found")
    with open(DATA_FILE,"r",encoding='utf-8') as file:
        return json.load(file)
    
def get_all_products() -> List[Dict]:
    return load_products()

def save_product(products:List[Dict])->None:
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(products,f,indent=2, ensure_ascii=False)
        
def add_product(product:Dict)->Dict:
    products = get_all_products()
    
    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("SKU already exists")
    
    products.append(product)
    save_product(products)
    return product

def delete_product(id:str) -> str:
    products = get_all_products()
    
    for idx, p in enumerate(products):
        if p["id"] == str(id):
            deleted = products.pop(idx)
            save_product(products)
            
    return {"message":"Product deleted successully","data":deleted}

def change_product(product_id:str, update_data:dict):
    products = get_all_products()
    for idx, product in enumerate(products):
        if product["id"] == str(product_id):

            for key, value in update_data.items():
                if value is None:
                    continue

                if (
                    # value is the new data which is dict and both the updated new data and previous data of a particular key should be dict
                    isinstance(value, dict)
                    and isinstance(product.get(key), dict)
                ):
                    # .update() dictionary ko merge ya modify karne ke liye use hota hai.
                    product[key].update(value)
                else:
                    product[key] = value

            products[idx] = product
            save_product(products)

            return product