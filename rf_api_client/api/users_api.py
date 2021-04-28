from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.users_api_models import CurrentUserDto, UserDto


class UsersApi(BaseApi):
    async def get_current(self) -> CurrentUserDto:
        url = self.context.base_url / 'api/user'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return CurrentUserDto(**body)

    async def get_by_id(self, user_id: str) -> UserDto:
        url = self.context.base_url / f'api/user/{user_id}'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return UserDto(**body)
