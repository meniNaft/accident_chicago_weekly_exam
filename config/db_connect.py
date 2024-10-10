import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection

load_dotenv()
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
taxi_db = client['chicago-accident']
accidents: Collection = taxi_db['accidents']
