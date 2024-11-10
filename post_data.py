from motor.motor_asyncio import AsyncIOMotorClient

async def post_dataMain(subject, scraped_data):
    # MongoDB connection details
    database_name = "TestDB"
    collection_name = "TestUser"

    # Create a MongoDB client
    client = AsyncIOMotorClient(f"mongodb://mad:123@10.141.31.247:27017/")

    # Access the database and collection
    db = client[database_name]
    collection = db[collection_name]

    # Insert a single document
    document = {
        "Type": "Scraped Data",
        "Subject": subject,
        "Data": scraped_data
    }

    result = await collection.insert_one(document)
    return result.inserted_id

async def delete_data(document_id):
    # MongoDB connection details
    database_name = "TestDB"
    collection_name = "TestUser"

    # Create a MongoDB client
    client = AsyncIOMotorClient(f"mongodb://mad:123@10.141.31.247:27017/")

    # Access the database and collection
    db = client[database_name]
    collection = db[collection_name]

    # Delete the document
    await collection.delete_one({"_id": document_id})