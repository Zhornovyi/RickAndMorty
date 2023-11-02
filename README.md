# RickAndMorty Integeration

1. Fetch the entire API contents for the objects: 
- Character 
- Location 
- Episode
2. Output all API objects to separate JSON files
3. Each JSON file should contain 3 fields:
   1. Id - generated guid
   2. Metadata - the name from within the fetched object
   3. RawData - The fetched JSON data presented as dictionary.
4. Upon finish, the program should print to the screen:
   1.  the list of names of the episodes aired between 2017 and 2021 and contains more than three characters.
   2.  the list of characters which appear only on odd episode numbers (episode 1, 3, 9 (of whatever season) ) 


## Installation
1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`

## Running

`python main.py`