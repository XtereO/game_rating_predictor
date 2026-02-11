import json
from games_api import RAWGamesAPI
from utils import data_path

def retrieve_train_games(max_size=1000, use_saved=False):
    return _retrieve_games(False, data_path["raw_games"], max_size, use_saved)

def retrieve_val_games(use_saved=False):
    return _retrieve_games(True, data_path["raw_val_games"], 20, use_saved)

def _retrieve_games(current_year, filepath, max_size=1000, use_saved=False):
    if(use_saved):
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            return data["games"]
    
    api = RAWGamesAPI()
    pull = lambda page: api.get_games_list_last_year(page)
    if(current_year):
        pull = lambda page: api.get_games_list_current_year(page)

    games = []
    try:
        page = 1
        while len(games)<max_size:
            data = pull(page)
            games+=data["results"]
            page+=1
            
            if(len(games)>=data["count"]): 
                break

    except RuntimeError as e:
        print("code error:\n", e)
        return
    
    with open(filepath, "w") as json_file:
        json.dump({"count": len(games), "games": games}, json_file, indent=2)

    return games
