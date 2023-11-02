import logging
import aiofiles
from os import path
from typing import List, Dict
from api.filters import ResourceFilter
from api.loader import ResourseLoader
from api.models import FileOutputObject
from aiohttp import ClientResponseError
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class RickAndMortyResource:
    def __init__(self,
                 base_url: str,
                 name: str,
                 model_class: BaseModel.__class__,
                 filters: Dict[str, ResourceFilter] = []):
        self.base_url = base_url
        self.name = name
        self.model_class = model_class
        self.filters = filters
        self.data: List[model_class] = []

    async def fetch(self, loader: ResourseLoader):
        res_url = path.join(self.base_url, self.name)
        try:
            raw_data = await loader.fetch_all_pages(res_url)
            self.data = [self.model_class(**item) for item in raw_data]
        except ClientResponseError as e:
            logger.error(f"An error occurred while loading {self.name}: {e}")
            raise e
        except ValidationError as e:
            logger.error(f"An error occurred while valudating response data {self.name}: {e}")
            raise e

    async def save(self, output_path='./'):
        if not path.exists(output_path):
            raise ValueError(f"Please provide valid dir path for saving {self.name}")
        data = FileOutputObject(metadata=self.name, raw_data=self.data)
        async with aiofiles.open(path.join(output_path, self.name + '.json'), "w") as f:
            await f.write(data.model_dump_json(indent=4))
        logger.info(f"Saved {self.name} to {output_path}")

    def filter_data(self, keys: List[str], **kwargs):
        if any(key not in self.filters for key in keys):
            raise ValueError(f"You can't filter resourse {self.name} with this keys {keys}")
        
        for item in self.data:
            if all(self.filters[key].apply(item, **kwargs) for key in keys):
                yield item

    async def fetch_and_save(self, loader: ResourseLoader, output_path='./'):
        await self.fetch(loader)
        await self.save(output_path) 