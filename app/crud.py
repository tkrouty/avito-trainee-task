from datetime import datetime, timedelta
from typing import Dict

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .models import Secret
from .encryption import Encryptor, hash_passphrase


async def insert_one_secret(db: AsyncIOMotorDatabase,
                            secret: Secret) -> str:
    """Sets secret's lifetime, encrypts its content
    and passphrase and creates a document in MongoDB.

    If lifetime is not specified, the according field for the document
    is not set and the document won't get deleted by Mongo's TTL monitor.
    """
    secret_doc = secret.dict()

    if secret.delete_after_minutes is not None:
        delta = timedelta(minutes=secret.delete_after_minutes)
        secret_doc['delete_at'] = datetime.utcnow() + delta

    del secret_doc['delete_after_minutes']
    enc = Encryptor()
    secret_doc['content'] = enc.encrypt(secret_doc['content'])
    secret_doc['passphrase'] = hash_passphrase(secret_doc['passphrase'])
    await db.secrets.insert_one(secret_doc)

    return str(secret_doc['_id'])


async def find_secret_by_id(db: AsyncIOMotorDatabase,
                            secret_key: str) -> Dict[str, str]:
    """Returns a document by its id and decrypts its content and passphrase."""

    obj_id = ObjectId(secret_key)
    result = await db.secrets.find_one({'_id': obj_id})
    if result is None or ('delete_at' in result
                          and result['delete_at'] <= datetime.utcnow()):
        return None

    enc = Encryptor()
    result['content'] = enc.decrypt(result['content'])

    return result
