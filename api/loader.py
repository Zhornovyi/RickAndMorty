import asyncio
import logging
from typing import List
from aiohttp import ClientSession, ClientError

logger = logging.getLogger(__name__)

class ResourseLoader():
    """Class to load concurrently all pages of API resource from a given URL."""
    def __init__(self, session: ClientSession):
        self.session = session

    async def get_total_pages(self, url: str) -> int:
        page = await self.fetch_page(url, 1)
        return page['info']['pages']

    async def fetch_page(self, url: str, page: int):
        try:
            async with self.session.get(url, params={'page': page}) as response:
                response.raise_for_status()  
                return await response.json()
        except ClientError as e:
            logger.error(f"An error occurred while fetching page {page}: {e}")
            raise e

    async def fetch_all_pages(self, url: str) -> List[dict]:
        total_pages = await self.get_total_pages(url)
        tasks = []
        for page in range(1, total_pages + 1):
            task = asyncio.ensure_future(self.fetch_page(url, page))
            tasks.append(task)
            responses = await asyncio.gather(*tasks)
        results = []
        for response in responses:
            if response:
                results.extend(response['results'])
        return results