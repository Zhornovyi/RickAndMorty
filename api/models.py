from pydantic import BaseModel, validator
from datetime import datetime
from uuid import uuid4, UUID
from typing import List

class RickAndMortyBaseModel(BaseModel):
    id: int
    name: str
    url: str
    created: str


class Character(RickAndMortyBaseModel):
    status: str
    species: str
    type: str
    gender: str
    origin: dict
    location: dict
    image: str
    episode: list


class Location(RickAndMortyBaseModel):
    type: str
    dimension: str
    residents: list
    

class Episode(RickAndMortyBaseModel):    
    air_date: datetime
    episode: str
    characters: list
   

    @validator('air_date', pre=True)
    def parse_air_date(cls, v):
        return datetime.strptime(v, '%B %d, %Y')
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%B %d, %Y')
        }


class FileOutputObject(BaseModel):
    id: UUID = uuid4()
    metadata: str
    raw_data: List[Character|Location|Episode]