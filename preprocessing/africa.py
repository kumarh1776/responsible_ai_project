"""Scripts to preprocess Africa survey data."""
from typing import List
import pandas as pd
import numpy as np
from pathlib import Path
from preprocessing.common_dictionaries import africa_columns_to_change
from preprocessing import mit

RAW_DATA_PATH = Path(__file__).parent.parent / "data/raw"
INTERMEDIATE_DATA_PATH = Path(__file__).parent.parent / "data/intermediate_data_files"
PREPROCESSING_PATH = Path(__file__).parent.parent / "preprocessing"
AFRICA_FILEPATH = RAW_DATA_PATH / "2023_rai_survey_africa_data_0221.xlsx"
MIT_FILEPATH = INTERMEDIATE_DATA_PATH / "2023_mit_global_data_cleaned_text.xlsx"


def load_from_excel(filepath: str) -> pd.DataFrame:
    """Load the raw data from Excel."""
    assert Path(filepath).exists(), f"Raw data for Africa not found in {filepath}"
    df_africa = pd.read_excel(filepath)

    # reformat survey questions and demographic questions to match MIT survey (mostly changing casing)
    df_africa = df_africa.rename(columns=africa_columns_to_change)

    # specifically change the pattern for Q21 to match that of the MIT survey
    question_21_pattern = r"(?P<question>Q21)(?P<number>[A-Z])(?P<remainder>_[0-9]+)"

    def question_21_formatter(match):
        """Reformat Q21A_1 to Q21_1_1"""
        output = match.group("question") + "_"
        if match.group("number"):
            lower_input = match.group("number").lower()
            text_to_number = ord(lower_input) - 96
            text_to_number = str(text_to_number)
            output = output + text_to_number
        if match.group("remainder"):
            output = output + match.group("remainder")
        return output

    df_africa.columns = df_africa.columns.str.replace(
        question_21_pattern, question_21_formatter, regex=True
    )

    # columns to drop
    other_drop_columns = [col for col in df_africa.columns if "Other" in col]
    capital_other_drop_columns = [col for col in df_africa.columns if "OTHER" in col]
    general_columns_to_delete = [
        "submitdate",
        "CountryDummy",
        "GenderFinal",
        "AgegroupFinal",
        "LocationFinal",
        "SecFinal",
    ]
    columns_to_delete_combined = (
        other_drop_columns + capital_other_drop_columns + general_columns_to_delete
    )
    df_africa.drop(columns=columns_to_delete_combined, inplace=True)

    # create dummy columns for missing ones
    df_africa["Duration(inseconds)"] = 1000
    df_africa["Finished"] = "TRUE"
    df_africa["Disclaimer"] = "I agree"
    df_africa["data_source"] = "Africa"

    # Error Corrections
    df_africa["Demo10"].astype(str)
    df_africa["Demo10"] = np.where(
        df_africa["Demo10"].str.contains("1999"), "10-99", df_africa["Demo10"]
    )

    print(f"Loaded {df_africa.shape[0]} rows from latest Sagaci (Africa) data.")
    print(df_africa.columns)
    df_africa.to_excel(INTERMEDIATE_DATA_PATH / "2023_africa_data_cleaned_text.xlsx")

# match_column_values is used to encode Africa binary columns in the same way as the MIT file
def match_column_values(df_mit: pd.DataFrame, df_africa: pd.DataFrame) -> pd.DataFrame:
    df_africa = pd.read_excel(
        INTERMEDIATE_DATA_PATH / "2023_africa_data_cleaned_text.xlsx"
    )
    pd.read_excel(MIT_FILEPATH)
    columns_to_exclude = [
        "Q6",
        "Q7",
        "Q12_1",
        "Q12_2",
        "Q12_3",
        "Q12_4",
        "Q12_5",
        "Q12_10",
        "Q27",
    ]
    # Match responses for Binary (Yes/No) columns in the Africa data based on the MIT data
    for col_name in df_africa.columns:
        columns_to_exclude = [
            "Q6",
            "Q7",
            "Q12_1",
            "Q12_2",
            "Q12_3",
            "Q12_4",
            "Q12_5",
            "Q12_10",
            "Q27",
        ]
        if df_mit[col_name].isnull().all():
            string_to_fill == ""
        elif col_name in columns_to_exclude:
            string_to_fill = df_africa[col_name]
        else:
            string_to_fill = df_mit.loc[df_mit[col_name].first_valid_index(), col_name]
        df_africa[col_name] = np.where(
            df_africa[col_name] == "Yes", string_to_fill, df_africa[col_name]
        )

    # Write out the path to the raw folder
    df_africa.to_excel(INTERMEDIATE_DATA_PATH / "2023_africa_data_cleaned_text.xlsx")
    return df_africa


load_from_excel(AFRICA_FILEPATH)
match_column_values(MIT_FILEPATH, AFRICA_FILEPATH)
