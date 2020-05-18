"""Testing basic API operations"""

from bson.objectid import ObjectId

import pytest

from app.crud import find_secret_by_id


@pytest.mark.asyncio
async def test_good_request(async_client, good_request, test_db):
    """Sends a correctly structured request and tests that a document in
    the database is created correctly.
    """
    response = await async_client.post("/generate", json=good_request)
    key = response.json()['secret_key']
    new_doc = await find_secret_by_id(test_db, ObjectId(key))

    assert response.status_code == 201
    assert new_doc is not None
    assert new_doc['content'] == "my content"


@pytest.mark.asyncio
async def test_bad_request(async_client, bad_request, test_db):
    """Sends an incorrectly structured request and checks that no documents
    were created as a result."""
    response = await async_client.post("/generate", json=bad_request)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_correct_return(async_client, key):
    """Uses a correct key, sends a correct passphrase and checks that
    server returns a correct secret.
    """
    response = await async_client.get("/secrets/" + key,
                                      params={"passphrase": "my passphrase"})

    assert response.status_code == 200
    assert response.json()["secret"] == "my content"


@pytest.mark.asyncio
async def test_wrong_key(async_client, key):
    """Uses an incorrect key and checks that server doesn't give away
    any secrets.
    """

    wrong_key = key + '!!'
    response = await async_client.get("/secrets/" + wrong_key,
                                      params={"passphrase": "my passphrase"})

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_wrong_passphrase(async_client, key):
    """Uses a correct key, but sends an incorrect passphrase and checks
    that server doesn't give away any secrets.
    """

    response = await async_client.get("/secrets/" + key,
                                      params={"passphrase": "bad passphrase"})

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_expired_secret(async_client, good_request):
    """Sends a request with lifetime = 0 and checks that server doesn't
    return it back when it's requested.
    """
    good_request['delete_after_minutes'] = 0
    response = await async_client.post("/generate", json=good_request)
    key = response.json()['secret_key']

    response = await async_client.get('/secrets/' + key,
                                      params={'passphrase': 'my passphrase'})

    assert response.status_code == 404
