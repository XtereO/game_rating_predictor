import pytest
import json
import pandas as pd

from reducing_games import reduce_games

# the script reads from root directory
raw_games_filepath = "./tests/raw_games_test.json"
reduced_games_filepath = "./tests/reduced_games_test.csv"

cols = ["id", "slug", "playtime", "platforms", "stores", "tags", "genres"]

@pytest.fixture(scope="session")
def test_raw_games():
    with open(raw_games_filepath, 'r') as json_file:
        data = json.load(json_file)
        return data["games"]
    
@pytest.fixture(scope="session")
def test_reduced_games():
    return pd.read_csv(reduced_games_filepath)

@pytest.fixture(scope="session")
def empty_reduced_games():
    return pd.DataFrame(columns=cols)

def test_raw_and_reduced_games_id(test_raw_games, test_reduced_games):
    for i, rg in enumerate(test_raw_games):
        assert rg["id"] == (test_reduced_games.loc[i, "id"])

@pytest.mark.parametrize("col", cols)
def test_reducing_empty_raw(empty_reduced_games, col):
    assert (reduce_games([]).loc[:, col] == empty_reduced_games.loc[:, col]).all()

@pytest.mark.parametrize("col", cols)
def test_reducing_game_cols(test_raw_games, test_reduced_games, col):
    reduced_games = reduce_games(test_raw_games)

    assert (reduced_games.loc[:, col] == test_reduced_games.loc[:, col]).all()
