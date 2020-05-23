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

        context = ApiContext(
            username=username,
            password=md5(password),
            base_url=base_url,
            read_timeout=read_timeout
        )

        self.users = UsersApi(context)
        self.maps = MapsApi(context)
        self.types = NodeTypesApi(context)
        self.nodes = NodesApi(context)
