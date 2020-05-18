import httpx
from motor.motor_asyncio import AsyncIOMotorClient
import pytest
from asgi_lifespan import LifespanManager

from app.config import MONGO_URL
from app.main import app
from app import db


@pytest.fixture
def good_request():
    """A request with all required fields filled."""
    return {"content": "my content",
            "passphrase": "my passphrase",
            }


@pytest.fixture
def good_request_with_lifetime(good_request):
    """A good request with specified lifetime."""
    good_request['delete_after_minutes'] = 0.05
    return good_request


@pytest.fixture
async def key(good_request, async_client):
    """Sends a good request and returns the key."""
    response = await async_client.post('/generate', json=good_request)
    key = response.json()['secret_key']
    return key


@pytest.fixture
def bad_request():
    """A request without any required fields"""
    return {"some field": "some_value"}


@pytest.fixture(scope='module')
async def test_db():
    """Creates a temporary database, sets a TTL index and
    returns a pymongo client.
    """
    client = AsyncIOMotorClient(MONGO_URL)
    client.test_db.secrets.create_index('delete_at',
                                        expireAfterSeconds=0)

    yield client.test_db

    client.drop_database('test_db')
    client.close()


@pytest.fixture(autouse=True)
def clear_test_collection(test_db):
    """Clears the testing collection after every test."""
    yield None
    test_db.secrets.delete_many({})


@pytest.fixture
async def _app():
    """Returns our ASGI app, that uses a temporary DB"""
    @app.on_event('startup')
    async def startup():
        db.conn.client = AsyncIOMotorClient(MONGO_URL)

    @app.on_event('shutdown')
    async def shutdown():
        db.conn.client.close()

    async def _get_test_db():
        return db.conn.client.test_db

    app.dependency_overrides[db.get_db] = _get_test_db

    async with LifespanManager(app):
        yield app


@pytest.fixture
async def async_client(_app):
    """An async client to send asynchronous requests direcly to our app."""
    async with httpx.AsyncClient(app=_app,
                                 base_url='http://app.io') as client:
        yield client
