import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils import prepare_reduced_games, load_model, models_path

def predict_games_ratings(data, include_ratings_plot=False):
    val_ratings = data.loc[:, "rating"] if "rating" in data.columns else pd.Series([])
    data = prepare_reduced_games(data)
    
    data_num_rows = data.shape[0]
    prediction_cols = data.columns
    training_cols_data = {}
    training_cols = pd.Series((pd.read_csv(models_path["training_cols"], header=None)).iloc[:,0])
    for col in training_cols:
        if col in prediction_cols:
            training_cols_data[col] = data.loc[:, col]
        else:
            training_cols_data[col] = pd.Series(np.zeros(data_num_rows), dtype="int")
    data = pd.DataFrame(training_cols_data)
    print(data.describe())
    if "rating" in data.columns:
        data = data.drop("rating", axis="columns")
    data = data.fillna(0)

    min_max_scaler = load_model(models_path["min_max_scaler"])
    data["playtime"] = min_max_scaler.transform(data[["playtime"]])

    pca = load_model(models_path["pca"])
    data = pca.transform(data)
    
    model = load_model(models_path["predicting_model"])
    ratings = pd.Series(model.predict(data))

    print(val_ratings.size, ratings.size)
    if(include_ratings_plot and val_ratings.size == ratings.size):
        show_ratings_plot(val_ratings, ratings)

    return ratings

def show_ratings_plot(val_ratings, pred_ratings):
    sns.lineplot(val_ratings, label="validation ratings")
    sns.lineplot(pred_ratings, label="predicted rating")
    plt.axhline(y=np.mean(pred_ratings), label="mean predicted ratings", color="orange", linestyle="--")

    plt.ylabel("Rating")
    plt.xlabel("Sample")
    plt.title("Ratings comparison")
    plt.legend()

    plt.show()