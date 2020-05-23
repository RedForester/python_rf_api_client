from aiohttp import ClientSession, BasicAuth

from rf_api_client.utils import md5
from rf_api_client.api.base_api import ApiContext
from rf_api_client.api.maps_api import MapsApi
from rf_api_client.api.node_types_api import NodeTypesApi
from rf_api_client.api.nodes_api import NodesApi
from rf_api_client.api.users_api import UsersApi

# todo inspect requests
# todo url builder
# todo ? cookie_jar


class RfApiClient:
    def __init__(self, *, username: str, password: str, base_url: str = "https://app.redforester.com", read_timeout: float = 60):
        self._context = ApiContext(
            username=username,
            password=md5(password),
            base_url=base_url,
            read_timeout=read_timeout
        )

        self._session = ClientSession(
            auth=BasicAuth(self._context.username, self._context.password),
            read_timeout=self._context.read_timeout,
            raise_for_status=True
        )

        self.users = UsersApi(self._session, self._context)
        self.maps = MapsApi(self._session, self._context)
        self.types = NodeTypesApi(self._session, self._context)
        self.nodes = NodesApi(self._session, self._context)

    @property
    def context(self):
        return self._context

    @property
    def session(self):
        return self._session

    async def __aenter__(self) -> 'RfApiClient':
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.__aexit__(exc_type, exc_val, exc_tb)

    async def close_session(self):
        """ Only if you using RfApiClient instance without context manager """
        await self._session.close()
