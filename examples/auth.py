import asyncio
import os

from rf_api_client import RfApiClient

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')


async def auth():
    async with RfApiClient(
        username=USERNAME,
        password=PASSWORD
    ) as api_client:
        user = await api_client.users.get_current()
        print('Current user is', user)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(auth())

    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
