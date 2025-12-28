from evaluation import evaluate_classification_model
from data_processing import get_prepared_data

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt

import joblib
import pickle
import os

def __save_model(model, filename: str):
    default_path = "./trained_models/classification/"
    full_name = default_path + filename + ".zlib"
    
    if os.path.exists(full_name):
        os.remove(full_name)

    with open(full_name, 'wb') as model_file:
        joblib.dump(model, model_file, compress='zlib')

def run_classification_models():
    X_train, X_test, y_train, y_test = get_prepared_data(database_url="postgresql://gms@localhost/mimiciv", classification=True)

    # Training XGBClassifier models with different learning rates
    print("------ XGBClassifier ------")
    for learning_rate in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]:
        model = XGBClassifier(n_estimators=3000, learning_rate=learning_rate, max_depth=6, random_state=1024)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        evaluation = evaluate_classification_model(y_test, y_pred)
        print(f"XGBClassifier - Learning Rate: {learning_rate} - Evaluation:", evaluation)
        print("-------------------------------")
        __save_model(model, f"xgb_lr_{str(learning_rate).replace('.', '_')}")

    print("*******************************")

    # # Training RandomForestClassifier models with different criteria
    # print("------ RandomForestClassifier ------")
    # for criterion in ['gini', 'entropy', 'log_loss']:
    #     model = RandomForestClassifier(n_estimators=3000, criterion=criterion, max_depth=6, random_state=1024)
    #     model.fit(X_train, y_train)
    #     y_pred = model.predict(X_test)
    #     evaluation = evaluate_classification_model(y_test, y_pred)
    #     print(f"RandomForestClassifier - {criterion} - Evaluation:", evaluation)
    #     print("-------------------------------")

    #     __save_model(model, f"random_forest_cr_{criterion}.pickle")

    # print("*******************************")

    # # Training LogisticRegression models with different solver and l1_ratio
    # print("------ LogisticRegression ------")
    # for l1_ratio in [0.0, 0.25, 0.5, 0.75, 1.0]:
    #     if l1_ratio == 0.0:
    #         for solver in ['lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag']:
    #             model = LogisticRegression(l1_ratio=l1_ratio, solver=solver, max_iter=10000, random_state=1024)
    #             model.fit(X_train, y_train)
    #             y_pred = model.predict(X_test)
    #             evaluation = evaluate_classification_model(y_test, y_pred)
    #             print(f"LogisticRegression - L1 Ratio: {l1_ratio} - Solver: {solver} - Evaluation:", evaluation)
    #             print("-------------------------------")
    #             __save_model(model, f"logistic_regression_l1r_{l1_ratio.replace('.', '_')}_solver_{solver}.pickle")

    #     elif l1_ratio == 1.0:
    #         model = LogisticRegression(l1_ratio=l1_ratio, solver='liblinear', max_iter=10000, random_state=42)
    #         model.fit(X_train, y_train)
    #         y_pred = model.predict(X_test)
    #         evaluation = evaluate_classification_model(y_test, y_pred)
    #         print(f"LogisticRegression - L1 Ratio: {l1_ratio} - Solver: liblinear - Evaluation:", evaluation)
    #         print("-------------------------------")
    #         __save_model(model, f"logistic_regression_l1r_{l1_ratio.replace('.', '_')}_solver_liblinear.pickle")

    #     model = LogisticRegression(l1_ratio=l1_ratio, solver='saga', max_iter=10000, random_state=42)
    #     model.fit(X_train, y_train)
    #     y_pred = model.predict(X_test)
    #     evaluation = evaluate_classification_model(y_test, y_pred)
    #     print(f"LogisticRegression - L1 Ratio: {l1_ratio} - Solver: saga - Evaluation:", evaluation)
    #     print("-------------------------------")
    #     __save_model(model, f"logistic_regression_l1r_{l1_ratio.replace('.', '_')}_solver_saga.pickle")

        # # Training SVC models with different kernels
        # print("------ SVC ------")
        # for kernel in ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']:
        #     model = SVC(kernel=kernel, random_state=1024)
        #     model.fit(X_train, y_train)
        #     y_pred = model.predict(X_test)
        #     evaluation = evaluate_classification_model(y_test, y_pred)
        #     print(f"SVC - {kernel} - Evaluation:", evaluation)
        #     print("-------------------------------")
        #     __save_model(model, f"svc_kernel_{kernel}.pickle")

    # cm = confusion_matrix(y_test, y_pred)

    # disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    # disp.plot()
    # plt.show()