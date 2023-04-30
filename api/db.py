from pymongo.mongo_client import MongoClient
from .configs import db_login, db_password

uri = f"mongodb+srv://{db_login}:{db_password}@cluster0.hzsg4od.mongodb.net/?retryWrites=true&w=majority"
db = MongoClient(uri).tasks