"""
This program will take the features from the first stage and the first stage model.
It will build a graph using the predictions from first stage and then extract graph features and
write them to csv files
"""
import numpy as np
import pandas as pd
from tqdm import tqdm
import joblib
from multiprocessing import Pool
import logging
from graph_tool.all import *
import warnings
import glob

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)

# initialize graph object which is shared by all cores
graph = Graph()
e_start = graph.new_ep("int")
e_end = graph.new_ep("int")
e_pred_weight = graph.new_ep("float")


def get_directed_mentor_mentee_graph(df):
    graph.add_edge_list(
        df[
            ["mentor_ai2id", "mentee_ai2id", "copub_end", "copub_start", "pred_prob"]
        ].values,
        eprops=[e_start, e_end, e_pred_weight],
    )


def divide_zero(num, den):
    if num == 0 or den == 0:
        return 0
    else:
        return num / den


def get_prediction_feature_dataframe(df, first_stage_model):
    """
    takes in either candidate mentor pairs or candidate mentee pairs of candidate mentors to predict
    probability of being a mentor
    :param file_name: feature files
    :param first_stage_model: pickle file for first stage pairwise model
    :return: dataframe with prediction(pred_prob) column
    """
    df_buffer = df[["mentee_ai2id", "mentor_ai2id", "copub_end", "copub_start",]]

    df = df.drop(["mentee_ai2id", "mentor_ai2id", "copub_end", "copub_start",], axis=1,)

    lgbm_pickle = joblib.load(first_stage_model)

    yhat = lgbm_pickle.predict_proba(df)
    probs = yhat[:, 1]
    pred_prob = pd.Series(probs, name="pred_prob")
    return pd.concat([df, pred_prob, df_buffer], axis=1)


def get_in_weights(ai2id, graph, copub_start, copub_end):
    """
    assumption: completely throws away in edges that are not in the copub period
    :param ai2id: ai2id of node
    :param graph: graph object
    :param copub_end: co-publication end date for the pair
    :return: a list of incoming prediction probability edge weights for an author
    """
    in_weights = []
    for mentor, mentee, end_date, weight in graph.iter_in_edges(
        ai2id, [e_end, e_pred_weight]
    ):
        if copub_start <= end_date <= copub_end:
            in_weights.append(weight)
    return in_weights


def get_out_weights(ai2id, graph, copub_start, copub_end):
    """
    assumption: completely throws away out edges that are not in the copub period
    :param ai2id: ai2id of node
    :param graph: graph object
    :param copub_end: co-publication end date for the pair
    :return: a list of outgoing prediction probability edge weights for an author
    """
    out_weights = []
    for mentor, mentee, end_date, weight in graph.iter_out_edges(
        ai2id, [e_end, e_pred_weight]
    ):
        if copub_start <= end_date <= copub_end:
            out_weights.append(weight)
    return out_weights


def get_graph_features(df):
    df["mte_in_weights"] = df.apply(
        lambda row: get_in_weights(
            row["mentee_ai2id"], graph, row["copub_start"], row["copub_end"]
        ),
        axis=1,
    )
    df["mte_out_weights"] = df.apply(
        lambda row: get_out_weights(
            row["mentee_ai2id"], graph, row["copub_start"], row["copub_end"]
        ),
        axis=1,
    )

    df["coa_in_weights"] = df.apply(
        lambda row: get_in_weights(
            row["mentor_ai2id"], graph, row["copub_start"], row["copub_end"]
        ),
        axis=1,
    )
    df["coa_out_weights"] = df.apply(
        lambda row: get_out_weights(
            row["mentor_ai2id"], graph, row["copub_start"], row["copub_end"]
        ),
        axis=1,
    )

    df["coa_out_min"] = df.apply(
        lambda row: np.min(row["coa_out_weights"], initial=1), axis=1
    )
    df["coa_in_min"] = df.apply(
        lambda row: np.min(row["coa_in_weights"], initial=1), axis=1
    )

    df["mte_out_min"] = df.apply(
        lambda row: np.min(row["mte_out_weights"], initial=1), axis=1
    )
    df["mte_in_min"] = df.apply(
        lambda row: np.min(row["mte_in_weights"], initial=1), axis=1
    )

    df["coa_out_max"] = df.apply(
        lambda row: np.max(row["coa_out_weights"], initial=0), axis=1
    )
    df["coa_in_max"] = df.apply(
        lambda row: np.max(row["coa_in_weights"], initial=0), axis=1
    )

    df["mte_out_max"] = df.apply(
        lambda row: np.max(row["mte_out_weights"], initial=0), axis=1
    )
    df["mte_in_max"] = df.apply(
        lambda row: np.max(row["mte_in_weights"], initial=0), axis=1
    )

    df["coa_out_sum"] = df.apply(lambda row: np.sum(row["coa_out_weights"]), axis=1)
    df["coa_in_sum"] = df.apply(lambda row: np.sum(row["coa_in_weights"]), axis=1)

    df["mte_out_sum"] = df.apply(lambda row: np.sum(row["mte_out_weights"]), axis=1)
    df["mte_in_sum"] = df.apply(lambda row: np.sum(row["mte_in_weights"]), axis=1)

    df["mte_weight_sum"] = df.apply(
        lambda row: row["mte_out_sum"] + row["mte_in_sum"], axis=1
    )
    df["coa_weight_sum"] = df.apply(
        lambda row: row["coa_out_sum"] + row["coa_in_sum"], axis=1
    )

    df["mte_ratio_in_out"] = df.apply(
        lambda row: divide_zero(row["mte_in_sum"], row["mte_out_sum"]), axis=1
    )
    df["coa_ratio_in_out"] = df.apply(
        lambda row: divide_zero(row["coa_in_sum"], row["coa_out_sum"]), axis=1
    )

    df["mte_avg_in"] = df.apply(lambda row: np.mean(row["mte_in_weights"]), axis=1)
    df["mte_avg_out"] = df.apply(lambda row: np.mean(row["mte_out_weights"]), axis=1)

    df["coa_avg_in"] = df.apply(lambda row: np.mean(row["coa_in_weights"]), axis=1)
    df["coa_avg_out"] = df.apply(lambda row: np.mean(row["coa_out_weights"]), axis=1)

    df = df.fillna(0)

    # drop the lists in the dataframe
    df = df.drop(
        ["mte_in_weights", "mte_out_weights", "coa_in_weights", "coa_out_weights"],
        axis=1,
    )

    return df


def read_features(directory):
    data = []
    logging.info("reading first stage features . . ")
    for filename in tqdm(glob.glob(directory + "*.csv")):
        df = pd.read_csv(filename, index_col=None, header=0)
        data.append(df)

    df = pd.concat(data, axis=0, ignore_index=True)
    return df


def parallelize_dataframe(df, func, n_cores):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df
