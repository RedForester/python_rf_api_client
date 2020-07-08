from types import SimpleNamespace
from uuid import uuid4

from aiohttp import ClientSession, BasicAuth, TraceConfig, TraceRequestStartParams, TraceRequestEndParams
from yarl import URL

from rf_api_client.api.base_api import ApiContext
from rf_api_client.api.maps_api import MapsApi
from rf_api_client.api.node_types_api import NodeTypesApi
from rf_api_client.api.nodes_api import NodesApi
from rf_api_client.api.notify_api import NotifyApi
from rf_api_client.api.users_api import UsersApi
from rf_api_client.log import main_logger as log
from rf_api_client.utils import md5

DEFAULT_RF_URL = URL('https://app.redforester.com')


class RfAuth:
    @property
    def username(self) -> str:
        raise NotImplementedError()

    @property
    def password(self) -> str:
        raise NotImplementedError()


class UserAuth(RfAuth):
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = md5(password)

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password


class ExtensionAuth(RfAuth):
    def __init__(self, token: str):
        self._token = token

    @property
    def username(self) -> str:
        return 'extension'

    @property
    def password(self) -> str:
        return self._token


class RfApiClient:
    def __init__(
            self,
            *,
            auth: RfAuth,
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
            username=auth.username,
            password=auth.password,
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
        self.notify = NotifyApi(self._session, self._context)

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
        trace_id = str(uuid4())[-6:]
        trace_config_ctx.trace_id = trace_id
        log.debug(f'Starting request [{trace_id}] with {params}')

    async def on_request_end(
            self,
            session: ClientSession,
            trace_config_ctx: SimpleNamespace,
            params: TraceRequestEndParams
    ):
        trace_id = trace_config_ctx.trace_id
        log.debug(f'Ending request [{trace_id}] {params}')
        if self._log_response_body:
            log.debug(await params.response.json())
