import asyncio
import logging
import os

from rf_api_client import RfApiClient
from rf_api_client.log import main_logger

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')


async def main():
    # set logging level
    logging.basicConfig(level=logging.DEBUG)
    main_logger.setLevel(logging.DEBUG)

    async with RfApiClient(
        username=USERNAME,
        password=PASSWORD,
        log_response_body=True  # log response bodies
    ) as api_client:
        user = await api_client.users.get_current()
        print('Current user is', user)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
