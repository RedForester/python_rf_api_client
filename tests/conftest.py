import pytest
from pydantic import BaseSettings
from yarl import URL

from rf_api_client import RfApiClient


class Secret(BaseSettings):
    developer_prefix: str = 'default'
    username: str = 'username'
    password: str = 'password'
    base_url: str = 'https://app.stage.redforester.com'

    class Config:
        env_prefix = 'rf_api_client_'


@pytest.fixture
def secret():
    return Secret()


@pytest.fixture
async def api(secret: Secret):
    async with RfApiClient(
        username=secret.username,
        password=secret.password,
        base_url=URL(secret.base_url)
    ) as api:
        yield api
