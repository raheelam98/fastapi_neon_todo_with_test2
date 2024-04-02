from starlette.config import Config
from starlette.datastructures import Secret
from starlette.testclient import TestClient

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL")
TEST_DATABASE_URL = config("TEST_DATABASE_URL")
