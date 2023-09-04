import pandas as pd
import numpy as np
from pathlib import Path
import uuid
import time
from preprocessing.common_dictionaries import INDUSTRY_TO_PRACTICE_AREA
from preprocessing.common_dictionaries import REGION_TO_COUNTRIES
from helper_functions import create_screener
from helper_functions import create_screener_without_demo4

INTERMEDIATE_DATA_PATH = Path(
    __file__).parent.parent / "data/intermediate_data_files"
UNIONED_FILEPATH = INTERMEDIATE_DATA_PATH / "initial_mastertable_2023.xlsx"
MASTER_DATA_PATH = Path(__file__).parent.parent / "data/master"

df = pd.read_excel(UNIONED_FILEPATH)


def create_q4_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Groups Q4 responses into groups based on an "any" membership of the subgroups.

    Args:
        df (pd.DataFrame): preprocessed combined data

    Returns:
        pd.DataFrame: preprocessed_combined data with Q4 groups
    """
    mapping = {
        "Broad principles": [
            ("Q14_1", "AI ethical standards"),
            ("Q14_2", "Human rights standards"),
            ("Q14_3", "Risk taxonomy"),
        ],
        "Policies": [
            ("Q14_4", "Policies and standards"),
        ],
        "Governance": [
            ("Q14_5", "Specific roles and responsibilities within the organization"),
            ("Q14_6", "Board of director expertise"),
            ("Q14_7", "External advisers/reviewers"),
            ("Q14_8", "Governance and escalation processes"),
            ("Q14_17", "Regulatory affairs"),
        ],
        "Monitoring": [
            ("Q14_10", "Ongoing monitoring and control for product-level risks"),
            (
                "Q14_11",
                "Ongoing monitoring and refinement of the RAI program",
            ),
            ("Q14_15", "Metrics and reporting"),
        ],
        "Tools and implementation": [
            ("Q14_9", "Integration into product development processes"),
            ("Q14_12", "Code libraries and software tools"),
            (
                "Q14_13",
                "Questionnaires, product risk assessments, product impact assessments",
            ),
        ],
        "Change management": [
            ("Q14_14", "Training and technical tutorials"),
            ("Q14_16", "Communication and cultural change"),
        ],
    }
    for idx, (key, value) in enumerate(mapping.items()):
        feature_name = f"Q14_grouped_{idx + 1}"
        cols = [col for col, _ in value]
        df[feature_name] = df[cols].notna().any(axis=1).map({True: key})

    return df


def create_q6_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Groups Q4 responses into groups based on an "any" membership of the subgroups.

    Args:
        df (pd.DataFrame): preprocessed combined data

    Returns:
        pd.DataFrame: preprocessed_combined data with Q4 groups
    """
    mapping = {
        "Transparency and explainability": [
            ("Q16_1", "Transparency"),
            ("Q16_2", "Explainability"),
        ],
        "Social and environmental impact": [
            ("Q16_3", "Social and environmental impact")
        ],
        "Accountability": [("Q16_4", "Accountability")],
        "Fairness": [("Q16_5", "Fairness and equity")],
        "Safety, security, and human wellbeing": [
            ("Q16_6", "Safety, security, and robustness"),
            ("Q16_10", "Human wellbeing"),
        ],
        "Data security and privacy": [
            ("Q16_7", "Data security/cybersecurity"),
            ("Q16_8", "Data privacy (data protection)"),
            ("Q16_9", "Individual/personal privacy"),
        ],
    }

    for idx, (key, value) in enumerate(mapping.items()):
        feature_name = f"Q16_grouped_{idx + 1}"
        cols = [col for col, _ in value]
        df[feature_name] = df[cols].notna().any(axis=1).map({True: key})

    return df


def unioned_file_other_fixes(unioned_df: pd.DataFrame) -> pd.DataFrame:

    # Add in screeners if it meets criteria to be included
    unioned_df = create_screener(unioned_df)
    unioned_df = create_screener_without_demo4(unioned_df)

    # Grouped Columns for certain Demo Questions
    country_to_region = {
        country: region
        for region, countries in REGION_TO_COUNTRIES.items()
        for country in countries
    }
    unioned_df['Demo 1_grouped'] = unioned_df['Demo1'].map(
        INDUSTRY_TO_PRACTICE_AREA)
    unioned_df['Demo 5_grouped'] = unioned_df['Demo5'].map(country_to_region)
    unioned_df['Demo 6_grouped'] = unioned_df['Demo6'].map(country_to_region)

    # Delete any unnecessary columns
    unioned_df.drop(columns=unioned_df.columns[0:2], axis=1, inplace=True)
    unioned_df = unioned_df[unioned_df.columns.drop(
        list(unioned_df.filter(regex='Q22_')))]
    # unioned_df.drop(columns = ["Q24b"], inplace = True)

    # Error handling
    unioned_df["Demo5"] = np.where(
        unioned_df["Demo5"] == "Egytp", "Egypt", unioned_df["Demo5"])
    unioned_df["Demo6"] = np.where(
        unioned_df["Demo6"] == "Egytp", "Egypt", unioned_df["Demo6"])
    unioned_df["Demo8"] = np.where(unioned_df["Demo8"] == "Prefer not to say/don’t know",
                                   "Prefer not to say/Don’t know", unioned_df["Demo8"])
    unioned_df = unioned_df.replace('e.g.', 'i.e.', regex=True)
    unioned_df = unioned_df.replace("I don't know", 'I dont know', regex=True)
    unioned_df = unioned_df.replace("I don’t know", 'I dont know', regex=True)
    unioned_df = unioned_df[unioned_df.ResponseId != "Response ID"]

    # Replace blanks to NaN
    unioned_df = unioned_df.replace(r'^\s*$', np.nan, regex=True)

    # Remove whitespace
    df_obj = unioned_df.select_dtypes(['object'])
    unioned_df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    # Rename Any relevant columns
    unioned_df.rename(columns={"Demo 1_grouped": "Demo1_grouped",
                               "Demo 5_grouped": "Demo5_grouped",
                               "Demo 6_grouped": "Demo6_grouped"
                               })
    return unioned_df


df = create_q4_groups(df)
df = create_q6_groups(df)
df = unioned_file_other_fixes(df)

# Add in a unique response Id for each row
df['ResponseId'] = [uuid.uuid4() for _ in range(len(df.index))]


def generate_multiselect_responses(
    df: pd.DataFrame
) -> pd.DataFrame:
    """ Generate multiselect tab for mastertable
    Args:
        df(pd.DataFrame): combined survey dataset for mastertable
    Returns: pd.DataFrame: Multiselect Responses tab for mastertable
    """
    multiselect_cols = [col for col in df if ('_' in col) and (
        "screener_without" not in col)]  # and ('grouped' not in col)]
    questions_tableau = multiselect_cols + ['ResponseId', 'screener']
    df_long = df[questions_tableau]
    df_long = df_long.melt(id_vars=['ResponseId', 'data_source', 'screener'],
                           var_name='Question_number', value_name='Answer').dropna()
    df_long['Question_number'] = df_long['Question_number'].str.split(
        '_').str[:-1].str.join('_')
    output = df_long[['ResponseId', 'Question_number', 'Answer']]
    return output


# Add a multiselect responses list as a new sheet
multiselect_responses = generate_multiselect_responses(df)

curr_time = time.strftime("%Y%m%d_%H%M")
file_name = "mastertable_2023_" + curr_time + ".xlsx"

with pd.ExcelWriter(MASTER_DATA_PATH / "mastertable_2023.xlsx") as writer:
    df.to_excel(writer, sheet_name='Combined Survey', index=False)
    multiselect_responses.to_excel(
        writer, sheet_name="Multiselect Responses", index=False)

with pd.ExcelWriter(MASTER_DATA_PATH / file_name) as writer:
    df.to_excel(writer, sheet_name='Combined Survey', index=False)
    multiselect_responses.to_excel(
        writer, sheet_name="Multiselect Responses", index=False)
