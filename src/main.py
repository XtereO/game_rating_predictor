import sys
from retrieving_games import retrieve_games
from reducing_games import reduce_games

use_saved = sys.argv[1] if len(sys.argv)>1 else 0
raw_games = retrieve_games(use_saved)

reduced_games = reduce_games(raw_games)
reduced_games.to_csv("reduced_games.csv", index=False)
