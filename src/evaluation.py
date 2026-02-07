
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score, f1_score, matthews_corrcoef
from sklearn.metrics import  mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.metrics import ConfusionMatrixDisplay, PredictionErrorDisplay

_default_path_classification = "./trained_models/classification/"
_default_path_regression = "./trained_models/regression/"

def plot_classification_confusion_matrix(y_true, y_pred, model_name: str):
    """
    Plot and save the confusion matrix for a classification model.

    Parameters:
    y_true (list or array): Real values.
    y_pred (list or array): Predicted values.
    model_name (str): Name of the model (used for saving the plot).
    """
    disp = ConfusionMatrixDisplay.from_predictions(y_true, y_pred, cmap=plt.cm.Blues)
    disp.ax_.set_title(f'Confusion Matrix - {model_name}')
    plt.savefig(f'{_default_path_classification}{model_name}_confusion_matrix.png')
    plt.close()

def plot_regression_prediction_error(y_true, y_pred, model_name: str):
    """
    Plot and save the prediction error for a regression model.

    Parameters:
    y_true (list or array): Real values.
    y_pred (list or array): Predicted values.
    model_name (str): Name of the model (used for saving the plot).
    """
    disp = PredictionErrorDisplay.from_predictions(y_true, y_pred)
    disp.ax_.set_title(f'Prediction Error - {model_name}')
    plt.savefig(f'{_default_path_regression}{model_name}_prediction_error.png')
    plt.close()

def evaluate_classification_model(y_true, y_pred):
    """
    Evaluate the performance of a classification model.

    Parameters:
    y_true (list or array): Real values.
    y_pred (list or array): Predicted values.

    Returns:
    dict: Dictionary containing the evaluation metrics.
    ACC: Accuracy
    Balanced_ACC: Balanced Accuracy
    AUC: Area under the curve
    F1: F1 score
    MCC: Matthews correlation coefficient
    """
    
    acc = accuracy_score(y_true= y_true, y_pred= y_pred)
    balanced_acc = balanced_accuracy_score(y_true= y_true, y_pred= y_pred)
    auc = roc_auc_score(y_true= y_true, y_score= y_pred)
    f1 = f1_score(y_true= y_true, y_pred= y_pred, average='macro')
    mcc = matthews_corrcoef(y_true= y_true, y_pred= y_pred)

    return {
        'ACC': round(acc, 5),
        'Balanced_ACC': round(balanced_acc, 5),
        'AUC': round(auc, 5),
        'F1': round(f1, 5),
        'MCC': round(mcc, 5)
    }


def evaluate_regression_model(y_true, y_pred):
    """
    Evaluate the performance of a regression model.

    Parameters:
    y_true (list or array): Real values.
    y_pred (list or array): Predicted values.
    
    Returns:
    dict: Dictionary containing the evaluation metrics.
    RMSE: Root Mean Squared Error
    MAE: Mean Absolute Error
    R2: R-squared Score
    """

    rmse = root_mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return {
        'RMSE': round(rmse, 5),
        'MAE': round(mae, 5),
        'R2': round(r2, 5)
    }

def evaluate_xgboost_feature_importance(feature_importances, feature_names, classification: bool):
    print(feature_importances)
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
    feature_importance_df.sort_values(by='Importance', ascending=False, inplace=True)
    plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
    plt.title('Feature Importance in XGBoost')
    plt.ylabel('Feature')
    plt.xlabel('Importance')
    plt.tight_layout()
    if classification:
        plt.savefig(f'{_default_path_classification}XGB_feature_importance.png')
    else:
        plt.savefig(f'{_default_path_regression}XGB_feature_importance.png')
    plt.close()