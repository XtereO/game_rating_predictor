import sys
from retrieving_games import retrieve_train_games, retrieve_val_games
from reducing_games import reduce_games
from training_model import train_model
from model_predictor import predict_games_ratings
from utils import data_path

max_size = 1000
train_use_saved = int(sys.argv[1]) if len(sys.argv)>1 else 1
raw_games = retrieve_train_games(max_size, train_use_saved)

reduced_games = reduce_games(raw_games)
reduced_games.to_csv(data_path["reduced_games"], index=False)

include_plots = False
train_model(include_plots)

val_use_saved = int(sys.argv[2]) if len(sys.argv)>2 else 1
raw_val_games = retrieve_val_games(val_use_saved)
reduced_val_games = reduce_games(raw_val_games)
reduced_val_games.to_csv(data_path["reduced_val_games"], index=False)

include_ratings_chart = False
ratings = predict_games_ratings(reduced_val_games, include_ratings_chart)
ratings.to_csv(data_path["predicted_val_games_ratings"], index=False, header=None)
