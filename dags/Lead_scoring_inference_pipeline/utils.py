"""
filename: utils.py
functions: encode_features, load_model
creator: veneesh
version: 1
"""

# Import necessary modules

import mlflow
import mlflow.sklearn
import pandas as pd
import sqlite3
import os
import logging
from datetime import datetime
from Lead_scoring_inference_pipeline.constants import *
from Lead_scoring_training_pipeline.constants import *
import time


def check_if_table_has_value(connection, table_name):

    # connection = sqlite3.connect(db_path+db_file_name)
    check_table = pd.read_sql(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';",
        connection,
    ).shape[0]
    return check_table == 1


# Define the function to train the model

def encode_features():
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH + DB_FILE_NAME)
        if not check_if_table_has_value(connection, "features"):
            _extracted_from_encode_features_24(connection)
        else:
            print("features already exists")
    except Exception as e:
        print(f"Error while running encode_features : {e}")
    finally:
        if connection:
            connection.close()


def _extracted_from_encode_features_24(connection):
    print("model_input Exists")
    df = pd.read_sql("select * from model_input", connection)

    # Implement these steps to prevent dimension mismatch during inference
    encoded_df = pd.DataFrame(columns=ONE_HOT_ENCODED_FEATURES)  # from constants.py
    placeholder_df = pd.DataFrame()

    # One-Hot Encoding using get_dummies for the specified categorical features
    for f in FEATURES_TO_ENCODE:
        if f in df.columns:
            encoded = pd.get_dummies(df[f])
            encoded = encoded.add_prefix(f + "_")
            placeholder_df = pd.concat([placeholder_df, encoded], axis=1)
        else:
            print("Feature not found")
            # return df

    # Implement these steps to prevent dimension mismatch during inference
    for feature in encoded_df.columns:
        if feature in df.columns:
            encoded_df[feature] = df[feature]
        if feature in placeholder_df.columns:
            encoded_df[feature] = placeholder_df[feature]

    encoded_df.fillna(0, inplace=True)

    encoded_df.to_sql(name="features", con=connection, if_exists="replace", index=False)
    print("features created/replaced")


# Define the function to load the model from mlflow model registry

def get_models_prediction():
    model_name = MODEL_NAME
    tag_value = TAG_VALUE
    connection = None
    try:
        mlflow.set_tracking_uri(TRACKING_URI)
        connection = sqlite3.connect(DB_PATH + DB_FILE_NAME)

        # Load model as a PyFuncModel.
        # As per the latest MLFlow documentations, the model_uri format has changed to the below
        # For more info, visit https://mlflow.org/docs/latest/model-registry.html#migrating-from-stages
        model_uri = f"models:/{model_name}@{tag_value}"
        print("Model url " + model_uri)
        loaded_model = mlflow.sklearn.load_model(model_uri)

        # Predict on a Pandas DataFrame.
        X = pd.read_sql("select * from features", connection)
        print("Making Prediction")
        predictions = loaded_model.predict(pd.DataFrame(X))
        pred_df = X.copy()

        pred_df["app_complete_flag"] = predictions
        pred_df.to_sql(
            name="predictions", con=connection, if_exists="replace", index=False
        )
        pred_df.to_csv(INFER_PATH)
        print("Predictions are done and create/replaced Table")
    except Exception as e:
        print(f"Error while running get_models_prediction : {e}")

# Define the function to check the distribution of output column

def prediction_ratio_check():
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH + DB_FILE_NAME)
        pred = pd.read_sql("select * from predictions", connection)
        pct_ones = round(
            pred["app_complete_flag"].sum() / pred["app_complete_flag"].count() * 100, 2
        )
        pct_zeroes = 100 - pct_ones
        with open(FILE_PATH, "a") as f:
            f.write(
                f"Prediction ratio for the date {time.ctime()} \n 1   {pct_ones}% \n 0   {pct_zeroes}%\n"
            )
        print(
            f"Prediction ratio for the date {time.ctime()} for Ones % {pct_ones} and Zeroes % {pct_zeroes}"
        )
    except Exception as e:
        print(f"Error while running prediction_ratio_check : {e}")


# Define the function to check the columns of input features

def input_features_check():
    connection = None
    try:
        # Creating an object
        logger = logging.getLogger()

        connection = sqlite3.connect(DB_PATH + DB_FILE_NAME)
        features = pd.read_sql("select * from features", connection)
        connection.close()

        if list(features.columns) == ONE_HOT_ENCODED_FEATURES:
            logger.info("All the models input are present")
        else:
            logger.error("Some of the models inputs are missing")
    except Exception as e:
        print(f"Error while running input_col_check : {e}")
    finally:
        if connection:
            connection.close()
