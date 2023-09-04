import os
from collections import Counter
from urllib import response
import warnings
import numpy as np
import pandas as pd
from itertools import chain
from sklearn.cluster import KMeans
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
import time
from openpyxl import load_workbook
from preprocessing.common_dictionaries import demo5_grouped_mapping_fixes
from preprocessing.common_dictionaries import demo6_grouped_mapping_fixes

"""
Maturity cluster definition: 0 - leader, 1 - non-leader 
Maturity score definition: sum(Q14) + sum(Q15) + sum(Q16). Max maturity score is 15. 
"""
RAW_DATA_PATH = Path(__file__).parent.parent / "data/master/middle_east_mastertable_2023_20230329_1237.xlsx"
OUTPUT_DATA_PATH = Path(__file__).parent.parent / "data/output/output_table_me.xlsx"

warnings.filterwarnings("ignore")
# load master table


def load_master_table(filepath: str = None) -> pd.DataFrame:
    """Loads mastertable as pandas dataframe
    Filter data to screened, drop entries where Q15 is null
    Args:
        filepath: path to mastertable
    Returns:
        pd.DataFrame: mastertable dataframe
    """
    master_table = pd.read_excel(filepath, sheet_name="Combined Survey", index_col=None)
    return master_table


def feature_engineering(df: pd.DataFrame, year: str, q: list[str]) -> pd.DataFrame:
    """Feature engineer selected columns to prepare data for clustering
    Filter data to screened, drop entries where Q15 is null
    Includes 2022 one-hot-encode and 2023 summation methods
    Args:
        df: Mastertable dataset
        year: the different encoding method used 2022 vs. 2023. One-hot-encode for 2022, and summation of
              counts for 2023
        q: List of features for clustering
    Returns:
        pd.DataFrame: dataframe with features processed ready for clustering
    """
    # encoding of q15
    q15_dict = {
        "Not at all": 0,
        "Ad hoc (i.e., team by team, project by project)": 1,
        "Partial (i.e., some business units)": 2,
        "Enterprisewide (i.e., mandatory policies)": 3,
        "I don't know": 0,
        "I don't know": 0,
    }
    df = df[(df["screener"] == "Yes")]
    df = df[df["Q15"].notna()]
    output = []
    for ques in q:
        # if this is a multiselect col
        if any((ques + "_") in col for col in df.columns):
            # we use the 2022 method (one hot encode Q14, Q15, Q16) for maturity cluster
            if year == "2022":
                cols = [col for col in data if ((ques + "_grouped") in col)]
                df = df.assign(**{col: df[col].notna().astype(int) for col in cols})
                output = output + cols
            # we use the 2023 method (adding up Q14, Q15, Q16) for maturity score
            elif year == "2023":
                df[ques] = df[
                    df.columns[pd.Series(df.columns).str.startswith(ques + "_grouped")]
                ].count(axis=1)
                df = df[df.columns.drop(list(df.filter(regex=(ques + "_grouped"))))]
                output.append(ques)
            else:
                print("wrong input")
                return
        elif ques == "Q15":
            df["Q15_mapped"] = df["Q15"].map(q15_dict)
            output = output + ["Q15_mapped"]
        else:
            pass

    return df[output]


def cluster_model(df: pd.DataFrame, n_cluster: int) -> pd.DataFrame:
    """Runs clustering model for processed features
    Replace all NaNs with 0
    Args:
        df: Dataframe with processed features
        n_cluster: number of desired clusters
    Returns:
        pd.DataFrame: dataframe with cluster label. The output of this model only contains
                      the 3 questions used for clustering, and the cluster label.
    """
    # replace NaN with 0
    df = df.fillna(0)
    kmeans = KMeans(
        n_clusters=n_cluster,
        init="k-means++",
        max_iter=300,
        n_init=10,
        random_state=2022,
    )
    y = kmeans.fit_predict(df)
    df["cluster"] = y
    return df


def relabel_cluster(df: pd.DataFrame) -> pd.DataFrame:
    """Change the label from 4 cluster to 2 cluster. Leader - maximum score for sum(Q14, Q15, Q16). Non-leader - rest
    of the clusters.
            Args:
                df: Dataframe with clustering output
            Returns:
                pd.DataFrame: dataframe with re-labeled cluster to leader vs. non-leader
    """
    # call preprocessed 2023
    eval = (
        preprocessed_2023.groupby("cluster")["Q14", "Q15_mapped", "Q16"]
        .mean()
        .reset_index()
    )
    eval["sum"] = eval["Q14"] + eval["Q15_mapped"] + eval["Q16"]
    max_cluster = int(eval.loc[eval["sum"] == eval["sum"].max(), "cluster"])
    preprocessed_2023["cluster"] = np.where(
        preprocessed_2023["cluster"].isin([max_cluster]), 0, 1
    )
    return df


def cluster_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the percentage of whole data point in each cluster.
    Args:
        df: Dataframe with cluster label
    Returns:
        pd.DataFrame: dataframe with percentage of datapoints within each cluster
    """
    output = df.groupby("cluster")["cluster"].count() / len(df)
    output1 = df.groupby("cluster")["cluster"].count()
    print(output1)
    return output


def visualization(df: pd.DataFrame, q: list[str]):
    """Visualization of the clusters (for 2023 method only)
    Args:
        df: Dataframe with cluster label
    Returns:
       visualization of the cluster
    """

    # The three dimensions are Q14, Q15 and Q16 used to create the clustering output.
    dim1 = q[0]
    dim2 = q[1]
    dim3 = q[2]
    c = Counter(zip(df[dim1], df[dim3]))
    weights = [80 * c[(xx, yy)] for xx, yy in zip(df[dim1], df[dim3])]
    sns.set(rc={"figure.figsize": (16, 12)})
    sns.scatterplot(
        data=df,
        x=df[dim1],
        y=df[dim3],
        c=df[dim2],
        cmap="Greens",
        style="cluster",
        s=weights,
        alpha=0.20,
        legend=False,
    )  # .set(title = "MIT Responses Q14,15,16 Clustered", xlabel='q14', ylabel='q16')
    plt.axis("off")
    plt.show()


# create function for assigning maturity score


def maturity_score(df: pd.DataFrame) -> pd.DataFrame:
    # assign maturity score
    df["maturity score"] = df["Q14"] + df["Q15_mapped"] + df["Q16"]
    return df


data = load_master_table(RAW_DATA_PATH)

# filter to exclude Middle East data
data = data[data["data_source"] != "Middle East"]
data = data[(data["screener"] == "Yes")]
data = data[data["Q15"].notna()]
data = data[data["Q15"] != "I dont know"]

# we use preprocessed_2022 to run the clustering model, and use preprocessed_2023 to generate maturity index
preprocessed_2022 = feature_engineering(data, "2022", ["Q14", "Q15", "Q16"])
preprocessed_2023 = feature_engineering(data, "2023", ["Q14", "Q15", "Q16"])
df_cluster_2022 = cluster_model(preprocessed_2022, 4)

preprocessed_2023["cluster"] = df_cluster_2022["cluster"]
output = relabel_cluster(preprocessed_2023)
output = maturity_score(output)
data = data.join(output)


# Adding additional columns for output file
cluster_mapping = {0: "Leader", 1: "Non-leader"}
data["rai_cluster"] = data["cluster"].map(cluster_mapping)

data["builder"] = np.where(
    data["Q1_1"].str.contains("Builds Own AI Tools", case=False, na=False), 1, 0
)

data["buyer"] = np.where(
    data["Q1_2"].str.contains("Buys/Licenses/Accesses AI Tools", case=False, na=False),
    1,
    0,
)

data["internal_failure"] = np.where(
    data["Q24b_1"].str.contains("AI system was internally built", case=False, na=False),
    1,
    0,
)

data["external_failure"] = np.where(
    data["Q24b_2"].str.contains(
        "AI system was externally bought, accessed, licensed", case=False, na=False
    ),
    1,
    0,
)

data["Demo 5_grouped"] = (
    data["Demo5"].map(demo5_grouped_mapping_fixes).fillna(data["Demo 5_grouped"])
)
data["Demo 6_grouped"] = (
    data["Demo6"].map(demo6_grouped_mapping_fixes).fillna(data["Demo 6_grouped"])
)

# Write out Output file to relevant folder
data.to_excel(OUTPUT_DATA_PATH)
# print(output)
