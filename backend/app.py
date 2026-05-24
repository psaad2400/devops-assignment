from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

mongo_host = os.getenv("MONGO_HOST", "mongodb")
client = MongoClient(f"mongodb://{mongo_host}:27017/")
db = client["testdb"]
collection = db["items"]

@app.route("/")
def home():
    return "Backend running"

@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    collection.insert_one(data)
    return "Created"

@app.route("/items", methods=["GET"])
def get_items():
    items = list(collection.find({}, {"_id": 0}))
    return jsonify(items)

@app.route("/items/<name>", methods=["DELETE"])
def delete_item(name):
    collection.delete_one({"name": name})
    return "Deleted"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)