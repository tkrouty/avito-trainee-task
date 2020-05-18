from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from . import api
from . import db
from .config import MONGO_URL, DB_NAME


app = FastAPI()

app.include_router(api.router)


@app.on_event("startup")
def connect_to_mongo():
    db.conn.client = AsyncIOMotorClient(MONGO_URL,
                                        minPoolSize=10,
                                        maxPoolSize=10)
    db.conn.client[DB_NAME].secrets.create_index('delete_at',
                                                 expireAfterSeconds=0)


@app.on_event("shutdown")
def close_mongo_connection():
    db.conn.client.close()
