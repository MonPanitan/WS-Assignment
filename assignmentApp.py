import requests
from fastapi import FastAPI
import json
from pydantic import BaseModel
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

import os

import base64

app = FastAPI()
client = MongoClient('mongodb://root:example@localhost:27017/')
db = client.autoStock
collection = db.itemList

API_KEY = os.getenv("CurrencyAPI")
print(API_KEY)

#pydantic model for the Item
class Item(BaseModel):
    ProductID: str
    Name: str
    Price: float
    Quantity: int
    Description: str
    letter: str #for startsWith function
    prodIDStart: str #for paginate function
    prodIDEnd: str #for paginate function

#Landing Page
@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Auto Parts API"}


#Pass a single ID number to get a single product
@app.get("/getSingleProduct/{id}")
def get_single_product(id):
    return json.loads(dumps(collection.find_one({'Product ID': id})))


#Get All Products
@app.get("/getAllProducts")
def get_all_products():
    return json.loads(dumps(collection.find()))


#Add new Product to the DB
@app.get("/addNewProduct/{prodID},{name},{price},{quantity},{description}")
def add_new_product(prodID, name, price, quantity, description):
    collection.insert_one({'Product ID': prodID, 'Name': name, 'Unit Price': price, 'Stock Quantity': quantity, 'Description': description})
    return {"message": "Product added successfully"}


#Delete Product from the DB
@app.get("/deleteProduct/{id}")
def delete_product(id):
    collection.delete_one({'Product ID': id})
    return({"message": "Product deleted successfully"})


#Get the Product that starts with a specific string/character
@app.get("/startsWith/{letter}")
def starts_with(letter):
    return json.loads(dumps(collection.find({'Name': {'$regex': '^' + letter}})))
    

#get the product in range of two product IDs(inclusive)
@app.get("/paginate/{prodIDStart},{prodIDEnd}")
def paginate(prodIDStart, prodIDEnd):
    return json.loads(dumps(collection.find({'Product ID': {'$gte': prodIDStart, '$lte': prodIDEnd}})))


#convertfrom USD to EUR
@app.get("/convert/{id}")
def convert(id):
    #get the exchange rate
    usdExchangeRate = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    response = requests.get(usdExchangeRate)
    data = response.json()
    
    #get EUR exchange
    euroConvertionRate = data.get('conversion_rates').get('EUR')

    #get the product from DB
    product = collection.find_one({'Product ID': id})
    
    #get the USD Unit Price attribute from product object
    usdCurr = product.get('Unit Price')

    #convert the USD to EUR
    convertedPrice = usdCurr * euroConvertionRate

    return ({"USD rate":usdCurr, "EUR exchange rate": euroConvertionRate, "EUR converted": "{:.2f}".format(convertedPrice)})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
