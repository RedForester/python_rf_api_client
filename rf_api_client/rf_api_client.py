from types import SimpleNamespace
from uuid import uuid4

from aiohttp import ClientSession, BasicAuth, TraceConfig, TraceRequestStartParams, TraceRequestEndParams
from yarl import URL

from rf_api_client.log import main_logger as log
from rf_api_client.utils import md5
from rf_api_client.api.base_api import ApiContext
from rf_api_client.api.maps_api import MapsApi
from rf_api_client.api.node_types_api import NodeTypesApi
from rf_api_client.api.nodes_api import NodesApi
from rf_api_client.api.users_api import UsersApi

# todo ? cookie_jar

DEFAULT_RF_URL = URL('https://app.redforester.com')


class RfApiClient:
    def __init__(
            self,
            *,
            username: str,
            password: str,
            session_id: str = None,
            base_url: URL = DEFAULT_RF_URL,
            read_timeout: float = 60,
            log_response_body=False,
    ):
        if session_id is None:
            session_id = str(uuid4())
            log.info(f'New session id is {session_id}')
        else:
            log.info(f'Supplied session id is {session_id}')

        self._context = ApiContext(
            username=username,
            password=md5(password),
            session_id=session_id,
            base_url=base_url,
            read_timeout=read_timeout
        )

        self._log_response_body = log_response_body

        self._session = ClientSession(
            auth=BasicAuth(self._context.username, self._context.password),
            read_timeout=self._context.read_timeout,
            headers={
                'SessionId': self._context.session_id,  # todo will be deprecated
                'Rf-Session-Id': self._context.session_id
            },
            trace_configs=[self.get_trace_config()],
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

    def get_trace_config(self):
        trace_config = TraceConfig()
        trace_config.on_request_start.append(self.on_request_start)
        trace_config.on_request_end.append(self.on_request_end)

        return trace_config

    async def on_request_start(
            self,
            session: ClientSession,
            trace_config_ctx: SimpleNamespace,
            params: TraceRequestStartParams
    ):
        log.debug(f'Starting request {params}')

    async def on_request_end(
            self,
            session: ClientSession,
            trace_config_ctx: SimpleNamespace,
            params: TraceRequestEndParams
    ):
        log.debug(f'Ending request {params}')
        if self._log_response_body:
            log.debug(await params.response.json())
