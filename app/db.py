from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection

from .config import DB_NAME


class DBConnection:
    client: AsyncIOMotorClient = None


conn = DBConnection()


def get_db() -> AsyncIOMotorCollection:
    """Returns a link to an object referring to the database."""
    return conn.client[DB_NAME]
