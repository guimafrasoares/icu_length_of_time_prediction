
from sklearn.model_selection import GridSearchCV
from utils import save_model
from evaluation import evaluate_classification_model, plot_classification_confusion_matrix

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

def __search_best_params(model, parameters, X_train, y_train, X_test, y_test, name: str):
    grid_search = GridSearchCV(estimator=model, param_grid=parameters, cv=3, scoring='accuracy', n_jobs= 4)
    grid_search.fit(X_train, y_train)
    print(f"Best score: {grid_search.best_score_:.3f}")
    print("Best Parameters:", grid_search.best_params_)
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    save_model(model=best_model, filename=f'{name}_best_model', model_type= "classification")

    evaluation = evaluate_classification_model(y_test, y_pred)
    print(f"{name} - Evaluation:", evaluation)
    plot_classification_confusion_matrix(y_test, y_pred, name)
    print("-------------------------------")

def train_xgb_classifier_model(X_train, y_train, X_test, y_test):
    print("------ XGB Classifier ------")
    # Define the hyperparameter distributions
    param_dist = {
        'max_depth': [3, 5, 7, 9],
        'learning_rate': [0.005, 0.01, 0.1, 0.15, 0.2, 0.25, 0.3],
        'n_estimators': [100, 200, 500, 1000]
    }
    __search_best_params(XGBClassifier(), param_dist, X_train, y_train, X_test, y_test, "XGB_Classifier")
    print("*******************************")

def train_random_forest_classifier_model(X_train, y_train, X_test, y_test):
    print("------ Random Forest Classifier ------")
    # Define the hyperparameter distributions
    param_dist = {
        'max_depth': [3, 5, 7, 9],
        'criterion': ['gini', 'entropy', 'log_loss'],
        'n_estimators': [100, 200, 500, 1000]
    }
    __search_best_params(RandomForestClassifier(), param_dist, X_train, y_train, X_test, y_test, "Random_Forest_Classifier")
    print("*******************************")

def train_logistic_regression_model(X_train, y_train, X_test, y_test):

    print("------ Logistic Regression ------")
    # Define the hyperparameter distributions
    param_dist = {
        'l1_ratio': [0.0],
        'solver': ['lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag'],
        'C': [0.0, 0.25, 0.5, 0.75, 1.0, 10.0, 100.0],
        'max_iter': [100000]
    }
    __search_best_params(LogisticRegression(), param_dist, X_train, y_train, X_test, y_test, "Logistic_Regression_L1_0")

    # Define the hyperparameter distributions
    param_dist = {
        'l1_ratio': [1.0],
        'solver': ['liblinear'],
        'C': [0.0, 0.25, 0.5, 0.75, 1.0, 10.0, 100.0],
        'max_iter': [100000]
    }
    __search_best_params(LogisticRegression(), param_dist, X_train, y_train, X_test, y_test, "Logistic_Regression_L1_1")
    print("*******************************")

def train_knn_classifier_model(X_train, y_train, X_test, y_test):
    print("------ KNN Classifier ------")
    # Define the hyperparameter distributions
    param_dist = {
        'n_neighbors': [3, 5, 7, 9, 11],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan', 'minkowski'],
        'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
    }
    __search_best_params(KNeighborsClassifier(), param_dist, X_train, y_train, X_test, y_test, "KNN_Classifier")
    print("*******************************")

