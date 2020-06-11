from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.users_api_models import CurrentUserDto


class UsersApi(BaseApi):
    async def get_current(self) -> CurrentUserDto:
        url = self.context.base_url / 'api/user'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return CurrentUserDto(**body)
