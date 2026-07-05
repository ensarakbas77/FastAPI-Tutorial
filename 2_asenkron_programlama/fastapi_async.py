# FastAPI ile Async Endpoint Yazmak
# Normal Endpoint vs Async Endpoint

import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Normal Endpoint",
        "type" : "Senkron" 
        }


@app.get("/asenkron")
async def home_async():

    await asyncio.sleep(5)  # 5 saniye bekle
    
    return {
        "message": "Asenkron Endpoint",
        "type" : "Asenkron",
        "situtaion" : "5 saniye bekledim"
        }