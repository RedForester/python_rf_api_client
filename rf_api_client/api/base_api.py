from aiohttp import ClientSession


class ApiContext:
    def __init__(self, *, username: str, password: str, base_url: str, read_timeout: float):
        self.username = username
        self.password = password
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
