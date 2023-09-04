"""this script preprocesses MIT data"""

import pandas as pd
import numpy as np
from pathlib import Path
from preprocessing.common_dictionaries import mit_columns_to_delete
from preprocessing.common_dictionaries import mit_columns_to_change
from preprocessing.common_dictionaries import multiselect_columns_to_delete
from preprocessing.helper_functions import multiselect_encoding

RAW_DATA_PATH = Path(__file__).parent.parent / "data/raw"
INTERMEDIATE_DATA_PATH = Path(__file__).parent.parent / "data/intermediate_data_files"
PREPROCESSING_PATH = Path(__file__).parent.parent / "preprocessing"
MIT_FILEPATH = RAW_DATA_PATH / "2023_rai_survey_mit_global_data_0223.xlsx"


def load_from_excel(filepath: str) -> pd.DataFrame:
    """Load the raw data from Excel."""
    assert Path(filepath).exists(), f"Raw data for MIT not found in {filepath}"
    df_mit = pd.read_excel(filepath)

    # Drop relevant columns
    df_mit.drop(columns=mit_columns_to_delete, inplace=True)

    # Use multiselect function to one-hot encode certain columns
    df_mit = multiselect_encoding(df_mit)

    # Rename relevant columns
    df_mit.rename(columns=mit_columns_to_change, inplace=True)

    # Add in a data_source column
    df_mit["data_source"] = "MIT"

    # Remove any spaces in column names
    df_mit.columns = df_mit.columns.str.replace(" ", "")

    # Drop the old multiselect columns
    df_mit.drop(columns=multiselect_columns_to_delete, inplace=True)
    df_mit.drop(columns=["Q24b"], inplace=True)

    # Write out the cleaned file to the data files folder
    # df_mit.to_excel(INTERMEDIATE_DATA_PATH /
    # "2023_mit_global_data_cleaned_text.xlsx")


load_from_excel(MIT_FILEPATH)
