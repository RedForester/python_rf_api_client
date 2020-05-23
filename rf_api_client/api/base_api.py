from aiohttp import ClientSession, BasicAuth


class ApiContext:
    def __init__(self, *, username: str, password: str, base_url: str, read_timeout: float):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.read_timeout = read_timeout


class BaseApi:
    def __init__(self, context: ApiContext):
        self._context = context

    def get_session(self):
        return ClientSession(
            auth=BasicAuth(self._context.username, self._context.password),
            read_timeout=self._context.read_timeout,
            raise_for_status=True
        )
