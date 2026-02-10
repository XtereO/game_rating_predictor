import joblib
import pandas as pd

models_path = {
    "min_max_scaler": "min_max_scaler.joblib",
    "pca": "pca.joblib",
    "predicting_model": "predicting_model.joblib"
}

def save_model(model, filepath):
    joblib.dump(model, filepath)

def load_model(filepath):
    return joblib.load(filepath)

def prepare_reduced_games(data):
    data = data.drop("id", axis="columns")
    if "rating" in data.columns:
        data["rating"] = (data["rating"]).astype(int)
        data = data.iloc[data["rating"]>0,:]

    folded_cols = ["platforms", "stores", "genres"]
    data = data.dropna(subset=folded_cols)
    data = data.dropna(subset=["rating", "playtime"])
    data["playtime"] = (data["playtime"]).astype(int)

    for fc in folded_cols:
        data = unfold_cols(data, fc)

    data_numeric = data.select_dtypes(include="number")

    return data_numeric

def unfold_cols(data, col):
    unique_cols = pd.Series(list(set((",".join(data.loc[:, col])).split(","))))
    print(f"column {col} has {unique_cols.size} values")

    temp = {}
    for c in unique_cols:
        values = (data[col].str.contains(c)).astype(int)
        temp[f"{col}_{c}"] = values

    data = pd.concat([data, pd.DataFrame(temp)], axis="columns")
    data = data.drop(col, axis="columns")

    return data