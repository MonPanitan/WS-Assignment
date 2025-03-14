from flask import Flask
from flask_restful import Api, Resource,reqparse
import json
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

import base64

app = Flask(__name__)
api = Api(app)

#Pass a single ID number to get a single product
class get_SingleProduct(Resource):
    def get(self, id):
        client = MongoClient('mongodb://localhost:27017/')
        db = client.auto
        collection = db.autoItemList
        result = collection.find_one({'Product ID': ObjectId(id)})
        return json.loads(dumps(result))
    
class get_AllProducts(Resource):
    def get(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client.auto
        collection = db.autoItemList
        result = collection.find()
        return json.loads(dumps(result))

class addNewProduct(Resource):
    def post(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client.auto
        collection = db.autoItemList
        parser = reqparse.RequestParser()
        parser.add_argument('Product ID', required=True)
        parser.add_argument('Name', required=True)
        parser.add_argument('Unit Price', required=True)
        parser.add_argument('Stock Quantity', required=True)
        parser.add_argument('Description', required=True)
        args = parser.parse_args()
        collection.insert_one(args)
        return {'message': 'Product added successfully'}
    
class deleteProduct(Resource):
    def delete(self, id):
        client = MongoClient('mongodb://localhost:27017/')
        db = client.auto
        collection = db.autoItemList
        collection.delete_one({'Product ID': ObjectId(id)})
        return {'message': 'Product deleted successfully'}
class startsWith(Resource):
    def get(self, name):
        client = MongoClient('mongodb://localhost:27017/')
        db = client.auto
        collection = db.autoItemList
        result = collection.find({'Name': {'$regex': '^' + name}})#Search for a product name and find the product that starts with letter entered in URL
        return json.loads(dumps(result))
class paginate(Resource):
    def get(self, page):
        client = MongoClient('mongodb://localhost:27017/')
        db = client.auto
        collection = db.autoItemList
        result = collection.find().skip((page - 1) * 10).limit(10)
        return json.loads(dumps(result))
    
class convert(Resource):
    def get(self, id):
        client = MongoClient('mongodb://localhost:27017/')
        db = client.auto
        collection = db.autoItemList
        result
    
api.add_resource(get_SingleProduct, "/getSingleProduct/<string:id>")

