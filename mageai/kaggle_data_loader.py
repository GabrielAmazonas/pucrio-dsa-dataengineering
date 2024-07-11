import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import os

@data_loader
def load_data_from_api(*args, **kwargs):
    # Initialize Kaggle API client
    api = KaggleApi()
    api.authenticate()  # Requires a valid Kaggle API key

    # Download dataset with unzip=True
    dataset_name = 'heesoo37/120-years-of-olympic-history-athletes-and-results'
    api.dataset_download_files(dataset_name, path='/default_repo/data_loaders', unzip=True)  # Download and unzip

    loaded_df = pd.read_csv('/default_repo/data_loaders/athlete_events.csv')

    # Displays general Information
    loaded_df.info()

    # Check for missing values in the DataFrame
    missing_values = loaded_df.isnull().sum()
    print("Missing Values:")
    print(missing_values)

    # Check for duplicate rows in the DataFrame
    duplicate_rows = loaded_df[loaded_df.duplicated()]
    print("Duplicate Rows:")
    print(duplicate_rows)

    # 1. Check for Missing Values

    return loaded_df


@test
def test_output(output, *args) -> None:
    """Q
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
