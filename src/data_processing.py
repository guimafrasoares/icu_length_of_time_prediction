import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def load_data(database_url):
    """
    Load data from the database.
    
    Parameters:
    database_url (str): Database connection URL.

    Returns -> DataFrame.
    """
    engine = create_engine(database_url)
    with engine.connect() as connection:
        df = pd.read_sql(sql="SELECT * FROM mimiciv_icu.full_patient_data WHERE careunit NOT LIKE 'NA' ORDER BY subject_id, stay_id, los;", con=connection)

    return df

def __preprocess_data(df, classification: bool):
    
    # Drop unecessary columns and rows with missing values
    df_simplified = df.drop(['subject_id', 'hadm_id', 'stay_id', 'intime', 'outtime'], axis=1)
    df_simplified = df_simplified.dropna()

    # Encode careunit column
    df_encoded = df_simplified.copy()
    careunit_mapping = {'NA': 0, 'MICU': 1, 'SICU': 2}
    df_encoded['careunit'] = df_encoded['careunit'].map(careunit_mapping)
    
    # Encode gender column
    gender_mapping = {'M': 0, 'F': 1}
    df_encoded['gender'] = df_encoded['gender'].map(gender_mapping)

    # Encode diagnosis columns
    diagnosis = np.concatenate((
        df_encoded['diagnosis_1'].unique(),
        df_encoded['diagnosis_2'].unique(),
        df_encoded['diagnosis_3'].unique()
    ))

    label_encoder = LabelEncoder()
    label_encoder.fit(diagnosis)

    df_encoded['diagnosis_1'] = label_encoder.transform(df_encoded['diagnosis_1'])
    df_encoded['diagnosis_2'] = label_encoder.transform(df_encoded['diagnosis_2'])
    df_encoded['diagnosis_3'] = label_encoder.transform(df_encoded['diagnosis_3'])

    # Encode target variable
    if classification:
        # For classification, label 'los' into 2 categories
        bins = [0, 4, float('inf')]
        labels = [0, 1]  # 0: <= 4 days, 1: > 4 days
        df_encoded['los'] = pd.cut(df_encoded['los'], bins=bins, labels=labels, right=True)

    else:
        df_encoded['los'] = df_encoded['los'].round(2)

    return df_encoded

def __split_data(df):
    dfx = df.drop(['los'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(dfx, df['los'], test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def get_prepared_data(database_url: str, classification: bool):
    """
    Get prepared data.
    
    Parameters:
    database_url (str): Database connection URL.
    classification (bool): Whether to perform classification or regression.
    
    Returns -> Tuple: X_train, X_test, y_train, y_test
    """
    df = load_data(database_url)
    df_processed = __preprocess_data(df, classification)
    X_train, X_test, y_train, y_test = __split_data(df_processed)
    return X_train, X_test, y_train, y_test