"""
Amaç: 
    - HTTPException
    - fastapi içinde hata döndürme, status code mantığını görme
"""

from itertools import product

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# örnek veri listesi
products = [
    {"id": 1, "name": "laptop", "price": 1000},
    {"id": 2, "name": "mouse", "price": 25},
    {"id": 3, "name": "keyboard", "price": 75}
]

# post isteği için model tanımı
class Product(BaseModel):
    id: int
    name: str
    price: float

# belirli bir ürünü getiren get endpointi
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
        
    # ürün bulunamazsa HTTPException fırlatılır
    raise HTTPException(status_code=404, detail="Ürün bulunamadı")


# yeni ürün ekleyen post endpointi
@app.post("/products")
async def create_product(product: Product):
    
    # aynı id var mı
    for item in products:
        if item["id"] == product.id:
            raise HTTPException(status_code=400, detail="Aynı ID'ye sahip ürün zaten mevcut")

    # fiyat kontrolü
    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Fiyat sıfırdan büyük olmalıdır")
    
    # yeni ürün ekle
    new_product = {"id": product.id, "name": product.name, "price": product.price}

    products.append(new_product)
    return {"message": "Ürün başarıyla eklendi", "product": new_product}