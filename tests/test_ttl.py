"""Testing that a ttl index is working as planned."""

import time

from bson.objectid import ObjectId

import pytest

from app.crud import find_secret_by_id


@pytest.mark.asyncio
async def test_ttl(async_client, test_db, good_request_with_lifetime):
    """Generates a doc with expiration time and waits for
    Mongo TTL Monitor to delete it.
    """
    response = await async_client.post("/generate",
                                       json=good_request_with_lifetime)
    key = response.json()['secret_key']

    new_doc = await find_secret_by_id(test_db, ObjectId(key))
    assert new_doc is not None

    time.sleep(60)

    new_doc = await find_secret_by_id(test_db, ObjectId(key))
    assert new_doc is None
