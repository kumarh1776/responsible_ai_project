"""Scripts to preprocess Sagaci (Africa) survey data."""
from typing import List
import pandas as pd
import numpy as np
from pathlib import Path
from preprocessing.common_dictionaries import china_columns_to_change

RAW_DATA_PATH = Path(__file__).parent.parent / "data/raw"
INTERMEDIATE_DATA_PATH = Path(__file__).parent.parent / "data/intermediate_data_files"
PREPROCESSING_PATH = Path(__file__).parent.parent / "preprocessing"
CHINA_FILEPATH = RAW_DATA_PATH / "2023_rai_survey_china_data_0224.xlsx"
MIT_FILEPATH = INTERMEDIATE_DATA_PATH / "2023_mit_global_data_cleaned_text.xlsx"


def load_from_excel(filepath: str) -> pd.DataFrame:
    """Load the raw data from Excel."""
    assert Path(filepath).exists(), f"Raw data for China not found in {filepath}"
    df_china = pd.read_excel(filepath)

    # reformat survey questions based on number of underscores
    df_china.columns = (df_china.columns.str.split().str[0]).str.replace(
        "__", "_", regex=False
    )

    # reformat Q3 to match the MIT survey
    question_3_pattern = r"(?P<question>Q3)(?P<number>_[0-9]+)(?P<remainder>_[0-9]+)"

    def question_3_formatter(match):
        """Reformat Q3_X_Y to Q3_Y_X"""
        output = match.group("question")
        if match.group("number") and match.group("remainder"):
            output = output + match.group("remainder") + match.group("number")
        return output

    df_china.columns = df_china.columns.str.replace(
        question_3_pattern, question_3_formatter, regex=True
    )

    # use list of columns found in common_dictionaries of case-by-case changing of China column names
    df_china = df_china.rename(columns=china_columns_to_change)

    # Create dummy columns to match that of MIT
    df_china["Finished"] = "TRUE"
    df_china["data_source"] = "China"
    df_china["RecordedDate"] = "2/16/2023 10:44:17"

    # Drop specific columns
    open_drop_columns = [col for col in df_china.columns if "open" in col]
    random_columns_to_drop = ["country_ip"]
    total_columns_to_drop = open_drop_columns + random_columns_to_drop
    df_china.drop(columns=total_columns_to_drop, inplace=True)

    print(f"Loaded {df_china.shape[0]} rows from latest China data.")
    print(df_china.columns)
    df_china.to_excel(INTERMEDIATE_DATA_PATH / "2023_china_data_cleaned_text.xlsx")

# match_column_values is used to encode Africa binary columns in the same way as the MIT file
def match_column_values(df_mit: pd.DataFrame, df_china: pd.DataFrame) -> pd.DataFrame:
    df_china = pd.read_excel(
        INTERMEDIATE_DATA_PATH / "2023_china_data_cleaned_text.xlsx"
    )
    df_mit = pd.read_excel(MIT_FILEPATH)
    for col_name in df_china.columns:
        if df_mit[col_name].isnull().all():
            string_to_fill == ""
        else:
            string_to_fill = df_mit.loc[df_mit[col_name].first_valid_index(), col_name]
        df_china[col_name] = np.where(
            df_china[col_name] == 1,
            string_to_fill,
            (np.where(df_china[col_name] == 0, "", df_china[col_name])),
        )
    df_china = df_china.replace("nan", "", regex=True)
    df_china.to_excel(INTERMEDIATE_DATA_PATH / "2023_china_data_cleaned_text.xlsx")
    return df_china


load_from_excel(CHINA_FILEPATH)
match_column_values(MIT_FILEPATH, CHINA_FILEPATH)
