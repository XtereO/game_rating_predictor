import json
from games_api import RAWGamesAPI

raw_games_filepath = "raw_games.json"
raw_test_games_filepath = "raw_test_games.json"

def retrieve_train_games(max_size=1000, use_saved=False):
    return _retrieve_games(False, raw_games_filepath, max_size, use_saved)

def retrieve_test_games(use_saved=False):
    return _retrieve_games(True, raw_test_games_filepath, 20, use_saved)

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
