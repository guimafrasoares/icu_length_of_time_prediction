
import os
from typing import Literal
import pickle

_file_extension = ".pkl"
_default_path_classification = "./trained_models/classification/"
_default_path_regression = "./trained_models/regression/"

def save_model(model, filename: str, model_type: Literal["classification", "regression"]):
    """
    Save trained model to disk.
    
    Parameters:
    model: The trained model to save.
    filename (str): The name of the file to save the model to.
    model_type: Type of the model - "classification" or "regression".
    """
    if model_type == "classification":
        full_name = _default_path_classification + filename + _file_extension
    elif model_type == "regression":
        full_name = _default_path_regression + filename + _file_extension
    else:
        raise ValueError("Invalid model type. Use 'classification' or 'regression'.")

    if os.path.exists(full_name):
        os.remove(full_name)
        
    with open(full_name, 'wb') as file:
        pickle.dump(model, file)


def load_model(model, filename: str, model_type: Literal["classification", "regression"]):
    """
    Load trained model from disk.
    
    Parameters:
    filename (str): Name of the file to load the model from.
    model_type: Type of the model - "classification" or "regression".

    Returns: Loaded model.
    """
    if model_type == "classification":
        full_name = _default_path_classification + filename + _file_extension
    elif model_type == "regression":
        full_name = _default_path_regression + filename + _file_extension
    else:
        raise ValueError("Invalid model type. Use 'classification' or 'regression'.")
    
    loaded_model = model.save_model(full_name)

    return model
