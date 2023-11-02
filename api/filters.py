from abc import ABC, abstractmethod
from .models import Episode

class ResourceFilter(ABC):
    @abstractmethod
    def apply(self, resource, **kwargs) -> bool:
        raise NotImplementedError()

class YearFilter(ResourceFilter):
    @classmethod
    def apply(cls, item: Episode, start_year: int = 0, end_year: int = 0,  **kwargs):
        if start_year == 0 and end_year == 0:
            return True
        return item.air_date.year in range(start_year, end_year+1)

class MinCharactersFilter(ResourceFilter):
    @classmethod
    def apply(cls, item: Episode, min_characters: int = 0,  **kwargs):
        if min_characters == 0:
            return True
        return len(item.characters) > min_characters
    
class OddEpisodeNumsFilter(ResourceFilter):
    @classmethod
    def apply(cls, item: Episode,  **kwargs):
        return item.id % 2 != 0