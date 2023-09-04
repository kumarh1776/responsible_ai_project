"""this script orchestrates all data ingestion functions"""
import pandas as pd
import numpy as np
from pathlib import Path


INTERMEDIATE_DATA_PATH = Path(__file__).parent.parent / "data/intermediate_data_files"
MIT_FILE_FOR_PROCESSING = (
    INTERMEDIATE_DATA_PATH / "2023_mit_global_data_cleaned_text.xlsx"
)
AFRICA_FILE_FOR_PROCESSING = (
    INTERMEDIATE_DATA_PATH / "2023_africa_data_cleaned_text.xlsx"
)
CHINA_FILE_FOR_PROCESSING = INTERMEDIATE_DATA_PATH / "2023_china_data_cleaned_text.xlsx"

from preprocessing import mit


def union(
    df_africa: pd.DataFrame, df_china: pd.DataFrame, df_mit: pd.DataFrame
) -> pd.DataFrame:
    df_africa = pd.read_excel(AFRICA_FILE_FOR_PROCESSING)
    df_mit = pd.read_excel(MIT_FILE_FOR_PROCESSING)
    df_china = pd.read_excel(CHINA_FILE_FOR_PROCESSING)

    # Concatenate all the dataframes
    unioned_df = pd.concat([df_africa, df_china, df_mit])

    # Write out file as mastertable
    unioned_df.to_excel(
        INTERMEDIATE_DATA_PATH / "initial_mastertable_2023.xlsx",
        sheet_name="Combined Survey",
        index=False,
    )


union(AFRICA_FILE_FOR_PROCESSING, CHINA_FILE_FOR_PROCESSING, MIT_FILE_FOR_PROCESSING)
