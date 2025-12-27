import pandas as pd
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
        df = pd.read_sql(sql="SELECT * FROM mimiciv_icu.full_patient_data;", con=connection)

    return df

def preprocess_data(df, classification: bool):
    # Round 'los' to 2 decimal places
    df['los'] = df['los'].round(2)

    # Drop unecessary columns
    df_simplified = df.drop(['subject_id', 'hadm_id', 'stay_id', 'intime', 'outtime'], axis=1)

    # Filter out rows with 'NA' careunit
    df_subset = df_simplified.loc[df_simplified['careunit'] != 'NA']
    df_subset = df_subset.dropna()
    
    # Encode categorical variables
    label_encoder = LabelEncoder()
    df_encoded = df_subset.copy()
    cat_cols = df_encoded.select_dtypes(include=['object']).columns

    for col in cat_cols:
        df_encoded[col] = label_encoder.fit_transform(df_encoded[col])

    if classification:
        # For classification, label 'los' into categories
        bins = [0, 1, 3, 7, float('inf')]
        labels = [0, 1, 2, 3]  # 0: <1 day, 1: 1-3 days, 2: 3-7 days, 3: >7 days
        df_encoded['los'] = pd.cut(df_encoded['los'], bins=bins, labels=labels, right=False)
        
        # Encode los column
        label_encoder = LabelEncoder()
        df_encoded['los'] = label_encoder.fit_transform(df_encoded['los'])
        
    return df_encoded

def split_data(df):
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
    df_processed = preprocess_data(df, classification)
    X_train, X_test, y_train, y_test = split_data(df_processed)
    return X_train, X_test, y_train, y_test