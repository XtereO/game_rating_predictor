import json
from games_api import RAWGamesAPI

def main():
    api = RAWGamesAPI()
    raw_games_filepath = "raw_games.json"

    try:
        games = api.get_games_list_last_year()
    except RuntimeError as e:
        print("code error:\n", e)
        return
    
    with open(raw_games_filepath, "w") as json_file:
        json.dump({"count": games["count"], "games": games["results"]}, json_file, indent=2)

    # and here we reduce games and then save them as .csv file

if __name__ == "__main__":
    main()