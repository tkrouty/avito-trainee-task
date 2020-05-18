import os


SECRET_KEY = os.getenv('SECRET_KEY',
                       'bxw3EgII8kiWgDZezsdJEGNqLL9Uhc1IJni3jzxUn38=').encode()


MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "password")

DB_NAME = os.getenv("MONGO_DB", "avito_task_db")

MONGO_URL = "mongodb://{0}:{1}@{2}:{3}/{4}".format(
    MONGO_USER,
    MONGO_PASSWORD,
    MONGO_HOST,
    MONGO_PORT,
    DB_NAME
)
