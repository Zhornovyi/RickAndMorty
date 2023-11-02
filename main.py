import time
import pprint
import asyncio
import logging
from aiohttp import ClientSession

from api import (
    ResourseLoader,
    YearFilter,
    OddEpisodeNumsFilter,
    MinCharactersFilter,
    RickAndMortyResource,
    Episode,
    Location,
    Character
) 


logging.basicConfig(level=logging.DEBUG, format='[%(name)s][%(levelname)s] - %(message)s')
logging.getLogger('asyncio').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


async def main():
    api_url = 'https://rickandmortyapi.com/api'
    
    episode_filters = {
        "year": YearFilter,
        "min_characters": MinCharactersFilter,
        "odd_episode_nums": OddEpisodeNumsFilter
    }
    
    resourses = {
        "character": RickAndMortyResource(base_url=api_url, name="character", model_class=Character),
        "location": RickAndMortyResource(base_url=api_url, name="location", model_class=Location),
        "episode": RickAndMortyResource(base_url=api_url, name="episode", model_class=Episode, filters=episode_filters),
    }
    
    async with ClientSession() as session:
        tasks = [res.fetch_and_save(ResourseLoader(session), './results') for res in resourses.values()]
        logger.debug("The fetching and saving has started")
        start = time.time() 
        await asyncio.gather(*tasks)
        logger.debug("The fetching has finished in %s seconds", time.time() - start)

    # Get all episodes between 2017 and 2021 with more than 3 characters  
    filtered_episodes = {}
    for ep in resourses['episode'].filter_data(keys=["year", "min_characters"], start_year=2017, end_year=2021, min_characters=3):
        filtered_episodes[ep.id] = ep.name
    logger.info("Episodes between %s and %s with more than %s characters: \n%s", 2017, 2021, 3, pprint.pformat(filtered_episodes))
    
    # Get all characters appeared in odd episodes
    filtered_characters = set()
    for ep in resourses['episode'].filter_data(keys=["odd_episode_nums"]):
        filtered_characters.update(ep.characters)
    logger.info("Characters appeared in odd episodes:\n%s", pprint.pformat(filtered_characters))


if __name__ == "__main__":
    asyncio.run(main())