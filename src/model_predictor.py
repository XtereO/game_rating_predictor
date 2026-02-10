from utils import prepare_reduced_games, load_model, models_path

def predict_games_ratings(data):
    data = prepare_reduced_games(data)
    if "rating" in data.columns:
        data = data.drop("rating", axis="columns")

    min_max_scaler = load_model(models_path["min_max_scaler"])
    data["playtime"] = min_max_scaler.transform(data[["playtime"]])
    pca = load_model(models_path["pca"])
    # use train cols of data (true if there is such value) - so write another prepare_reduced_games including train_cols
    data = pca.transform(data)
    
    model = load_model(models_path["predicting_model"])
    ratings = model.predict(data)

    return ratings
