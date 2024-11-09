from pymongo import MongoClient

username = "mad"
password = "123"
host = "localhost"
port = 27017
database_name = "TestDB"
collection_name = "TestUser"

client = MongoClient(f"mongodb://mad:123@10.141.31.247:27017/")

db = client[database_name]
collection = db[collection_name]

try:
    documents = collection.find()  # Retrieves all documents in the collection
    for document in documents:
        print(document)
except Exception as e:
    print("An error occurred:", e)
finally:
    client.close()  # Close the MongoDB connection