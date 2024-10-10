import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection

load_dotenv()
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
chicago_accident_db = client['chicago-accident']
accidents: Collection = chicago_accident_db['accidents']
