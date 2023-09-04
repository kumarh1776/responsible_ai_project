"""this script preprocesses middle east data"""

import pandas as pd
import numpy as np
from pathlib import Path
from preprocessing.common_dictionaries import middle_east_columns_to_delete
from preprocessing.common_dictionaries import middle_east_columns_to_change
from preprocessing.common_dictionaries import multiselect_columns_to_delete
from preprocessing.helper_functions import multiselect_encoding

RAW_DATA_PATH = Path(__file__).parent.parent / "data/raw"
INTERMEDIATE_DATA_PATH = Path(__file__).parent.parent / "data/intermediate_data_files"
PREPROCESSING_PATH = Path(__file__).parent.parent / "preprocessing"
MIDDLE_EAST_FILEPATH = RAW_DATA_PATH / "2023_rai_survey_middle_east_data_0221.xlsx"


def load_from_excel(filepath: str) -> pd.DataFrame:
    """Load the raw data from Excel."""
    assert Path(filepath).exists(), f"Raw data for Middle East not found in {filepath}"
    df_middle_east = pd.read_excel(filepath)

    # Drop relevant columns
    df_middle_east.drop(columns=middle_east_columns_to_delete, inplace=True)

    # Use multiselect function to one-hot encode certain columns
    df_middle_east = multiselect_encoding(df_middle_east)

    # Rename relevant columns
    df_middle_east.rename(columns=middle_east_columns_to_change, inplace=True)

    # Add in a data_source column
    df_middle_east["data_source"] = "Middle East"

    # Remove any spaces in column names
    df_middle_east.columns = df_middle_east.columns.str.replace(" ", "")

    # Drop the old multiselect columns
    df_middle_east.drop(columns=multiselect_columns_to_delete, inplace=True)
    df_middle_east.drop(columns=["Q24b"], inplace=True)

    # Write out the cleaned file to the data files folder
    df_middle_east.to_excel(
        INTERMEDIATE_DATA_PATH / "2023_middle_east_data_cleaned_text.xlsx"
    )


load_from_excel(MIDDLE_EAST_FILEPATH)
