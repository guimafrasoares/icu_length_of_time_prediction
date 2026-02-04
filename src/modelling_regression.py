
from utils import save_model
from evaluation import evaluate_regression_model, plot_regression_prediction_error

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor

def __search_best_params(model, parameters, X_train, y_train, X_test, y_test, name: str):
    grid_search = GridSearchCV(estimator=model, param_grid=parameters, cv=3, scoring='neg_root_mean_squared_error', n_jobs= 4)
    grid_search.fit(X_train, y_train)
    print(f"Best score: {grid_search.best_score_:.3f}")
    print("Best Parameters:", grid_search.best_params_)
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    save_model(model=best_model, filename=f'{name}_best_model', model_type= "regression")

    evaluation = evaluate_regression_model(y_test, y_pred)
    print(f"{name} - Evaluation:", evaluation)
    plot_regression_prediction_error(y_test, y_pred, name)
    print("-------------------------------")

def train_xgb_regressor_model(X_train, y_train, X_test, y_test):
    print("------ XGB Regressor ------")
    # Define the hyperparameter distributions
    param_dist = {
        'max_depth': [3, 5, 7, 9],
        'learning_rate': [0.005, 0.01, 0.05, 0.1],
        'subsample': [0.2, 0.4, 0.6, 0.8, 1.0],
        'n_estimators': [100, 200, 500, 1000]
    }
    __search_best_params(XGBRegressor(), param_dist, X_train, y_train, X_test, y_test, "XGB_Regressor")
    print("*******************************")

def train_random_forest_regressor_model(X_train, y_train, X_test, y_test):
    print("------ Random Forest Regressor ------")
    # Define the hyperparameter distributions
    param_dist = {
        'max_depth': [3],
        'criterion': ['squared_error', 'absolute_error', 'friedman_mse', 'poisson'],
        'n_estimators': [100, 200, 500, 1000]
    }
    __search_best_params(RandomForestRegressor(), param_dist, X_train, y_train, X_test, y_test, "Random_Forest_Regressor")
    print("*******************************")

def train_linear_regressor_model(X_train, y_train, X_test, y_test):
    print("------ Linear Regression ------")
    # Define the hyperparameter distributions
    param_dist = {
        'fit_intercept': [True, False],
        'copy_X': [True, False],
        'positive': [True, False]
    }
    __search_best_params(LinearRegression(), param_dist, X_train, y_train, X_test, y_test, "Linear_Regression")
    print("*******************************")

def train_knn_regressor_model(X_train, y_train, X_test, y_test):
    print("------ KNN Regressor ------")
    # Define the hyperparameter distributions
    param_dist = {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['uniform', 'distance'],
        'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
    }
    __search_best_params(KNeighborsRegressor(), param_dist, X_train, y_train, X_test, y_test, "KNN_Regressor")
    print("*******************************")

    