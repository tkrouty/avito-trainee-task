from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection

from .config import DB_NAME


class DBConnection:
    client: AsyncIOMotorClient = None


conn = DBConnection()


def get_db() -> AsyncIOMotorCollection:
    return conn.client[DB_NAME]
