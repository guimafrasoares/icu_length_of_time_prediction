from sklearn.metrics import accuracy_score, roc_auc_score, matthews_corrcoef, balanced_accuracy_score, r2_score, f1_score
from sklearn.metrics import  mean_absolute_error, mean_squared_error, root_mean_squared_error, mean_absolute_percentage_error

def avaliar_classificacao(y_true, y_pred):
    """
    Avalia o desempenho de um modelo de classificação.

    Parâmetros:
    y_true (list ou array): Valores reais das classes.
    y_pred (list ou array): Valores previstos pelo modelo.

    Retorna:
    dict: Dicionário contendo as métricas de avaliação.
    ACC: Accuracy
    Balanced_ACC: Balanced Accuracy
    AUC: Area Under the Curve
    F1: F1 Score
    MCC: Matthews Correlation Coefficient
    """
    accuracy = accuracy_score(y_true, y_pred)
    balanced_accuracy = balanced_accuracy_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    mcc = matthews_corrcoef(y_true, y_pred)

    return {
        'ACC': accuracy,
        'Balanced_ACC': balanced_accuracy,
        'AUC': auc,
        'F1': f1,
        'MCC': mcc
    }


def avaliar_regressao(y_true, y_pred):
    """
    Avalia o desempenho de um modelo de regressão.

    Parâmetros:
    y_true (list ou array): Valores reais das classes.
    y_pred (list ou array): Valores previstos pelo modelo.

    Retorna:
    dict: Dicionário contendo as métricas de avaliação.
    RMSE: Root Mean Squared Error
    MAE: Mean Absolute Error
    MAPE: Mean Absolute Percentage Error
    R2: R-squared Score
    """

    rmse = root_mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return {
        'RMSE': rmse,
        'MAE': mae,
        'MAPE': mape,
        'R2': r2
    }