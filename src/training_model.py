import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor

from utils import prepare_reduced_games, save_model, models_path, data_path

def train_model(include_plots=False):
    data = pd.read_csv(data_path["reduced_games"])
    data_numeric = prepare_reduced_games(data)
    print(data_numeric.describe())
    (pd.Series(data_numeric.columns)).to_csv(models_path["training_cols"], index=False, header=None)

    if (include_plots):
        show_plots(data_numeric)

    scaler = MinMaxScaler()
    data_numeric["playtime"] = scaler.fit_transform(data_numeric[["playtime"]])
    save_model(scaler, models_path["min_max_scaler"])

    y = data_numeric["rating"]    
    X = data_numeric.drop(axis="columns", columns=["rating"])
    pca = PCA(n_components=0.9)
    X = pca.fit_transform(X)
    save_model(pca, models_path["pca"])
    print("pca params:", pca.n_components_, pca.explained_variance_ratio_, pca.components_)

    rs = 17
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=rs)
    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=rs),
        'Random Forest': RandomForestRegressor(random_state=rs),
        'Support Vector Regression Poly': SVR(kernel="poly"),
        'Support Vector Regression RBF': SVR(kernel="rbf")
    }
    results = {}

    for model_name, model in models.items():
        pipeline = Pipeline(steps=[('model', model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        results[model_name] = {"mse": mse, "r2": r2}

    print(results)
    best_model = models[min(results.items(), key=lambda r: r[1]["mse"])[0]]
    print("the best model is", best_model)
    save_model(best_model, models_path["predicting_model"])

    return best_model

def show_plots(data):
    correlation_matrix = data.corr()
    print(correlation_matrix)

    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm',
                square=True, cbar_kws={"shrink": .8})

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.title('Correlation Matrix Heatmap')
    plt.tight_layout()
    plt.show()

    cols = data.columns
    hist_cols =  ["platforms", "stores", "genres"]
    for hc in hist_cols:
        x_cols = filter(lambda c: c.split("_")[0]==hc, cols)
        bar_data = (data.loc[:, x_cols]).sum()
        sns.barplot(data=bar_data)
        plt.title(f"{hc} distribution")
        plt.xticks(rotation=90)
        plt.ylabel("number of games")
        plt.show()

if __name__ == "__main__":
    include_correlation_matrix = sys.argv[1] if len(sys.argv) > 1 else False
    train_model(include_correlation_matrix)
