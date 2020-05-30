from aiohttp import ClientSession
from yarl import URL


class ApiContext:
    def __init__(self, *, username: str, password: str, session_id: str, base_url: URL, read_timeout: float):
        self.username = username
        self.password = password
        self.session_id = session_id
        self.base_url = base_url
        self.read_timeout = read_timeout


class BaseApi:
    def __init__(self, session: ClientSession, context: ApiContext):
        self._session = session
        self._context = context

    @property
    def session(self):
        return self._session

    @property
    def context(self):
        return self._context
