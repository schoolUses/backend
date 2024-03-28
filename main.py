import json
from fastapi import FastAPI, HTTPException
from flask import jsonify
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

mongo_url = "mongodb+srv://domdypol:Dompol19@cluster0.hxrw0cv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_url)
db = client["flipbird"]
collection = db["flipboard"]

f = open("db.json")

Users = json.load(f)

class Product(BaseModel):
    name: str
    price: float

@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.get("/users")
async def get_all_users():
    return Users

@app.get("/board/{board_id}")
def get_board(board_id: int):
    board = collection.find_one({"board_id": board_id}, {"board_id": 0})
    if board:
        return board
    else:
        raise HTTPException(status_code=404, detail="Product not found")



@app.get("/products/", response_model=list[Product])
def get_all_products():
    return list(collection.find())

@app.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    product = collection.find_one({"id": product_id}, {"_id": 0})
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products/", response_model=dict)
def add_product(product: Product):
    product_dict = product.dict()
    product_id = collection.insert_one(product_dict).inserted_id
    return {"id": product_id}

@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int):
    result = collection.delete_one({"id": product_id})
    if result.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=dict)
def update_product(product_id: int, product: Product):
    product_dict = product.dict()
    update_data = {"$set": product_dict}
    result = collection.update_one({"id": product_id}, update_data)
    if result.modified_count == 1:
        return {"message": "Product updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    
f.close()
