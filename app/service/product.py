import json
from pathlib import Path
from typing import List, Dict
from fastapi import HTTPException

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "products.json"

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        raise HTTPException(status_code=404, detail="No product found")
    with open(DATA_FILE,"r",encoding='utf-8') as file:
        return json.load(file)
    
def get_all_products() -> List[Dict]:
    return load_products()