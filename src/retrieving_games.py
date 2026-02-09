import json
from games_api import RAWGamesAPI

def retrieve_games(use_saved=False):
    raw_games_filepath = "raw_games.json"
    if(use_saved):
        with open(raw_games_filepath, 'r') as json_file:
            data = json.load(json_file)
            return data["games"]
    
    api = RAWGamesAPI()

    try:
        data = api.get_games_list_last_year()
    except RuntimeError as e:
        print("code error:\n", e)
        return
    
    games = data["results"]
    with open(raw_games_filepath, "w") as json_file:
        json.dump({"count": data["count"], "games": games}, json_file, indent=2)

    return games
