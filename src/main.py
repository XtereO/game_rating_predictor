import sys
from retrieving_games import retrieve_train_games, retrieve_test_games
from reducing_games import reduce_games
from training_model import train_model
from model_predictor import predict_games_ratings

max_size = 1000
train_use_saved = int(sys.argv[1]) if len(sys.argv)>1 else 1
raw_games = retrieve_train_games(max_size, train_use_saved)

reduced_games = reduce_games(raw_games)
reduced_games.to_csv("reduced_games.csv", index=False)

include_matrix_correlation = False
train_model(include_matrix_correlation)

test_use_saved = int(sys.argv[2]) if len(sys.argv)>2 else 1
raw_test_games = retrieve_test_games(test_use_saved)
reduced_test_games = reduce_games(raw_test_games)
reduced_test_games.to_csv("reduced_test_games.csv", index=False)

ratings = predict_games_ratings(reduced_test_games)
ratings.to_csv("predicted_test_games_ratings.csv", index=False)
