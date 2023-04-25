from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from configs import db_login, db_password

uri = f"mongodb+srv://{db_login}:{db_password}@cluster0.hzsg4od.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

