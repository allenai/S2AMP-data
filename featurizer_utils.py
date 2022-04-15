import numpy as np
from scipy.optimize import fmin

# THRESHOLD_DENSITY more will increase the copub period and will try to include all pubs and less with decrease
THRESHOLD_DENSITY = 0.6


def get_dense_period(years, thresh=THRESHOLD_DENSITY):
    points = np.array(years)  # should be a numpy array
    a, b = points.min(), points.max()

    def nlf(params):
        c, d = params
        within = ((points > c) & (points < d)).sum()
        return -np.log(1 / (d - c) + 1 / (b - a)) * within - np.log(1 / (b - a)) * (
            len(points) - within
        )

    res = fmin(
        nlf, (thresh * a + (1 - thresh) * b, (1 - thresh) * a + thresh * b), disp=0
    )
    return np.rint(res)


def get_count_range(list_dates, low, high):
    """
    returns count of years in list_dates between low and high
    """
    x = np.array(list_dates)
    return np.sum((low <= x) & (x <= high))


def get_count_years(list_count_year, date):
    coauthor_count = 0
    for _, tuple_count_year in enumerate(list_count_year):
        count = tuple_count_year[0]
        year = tuple_count_year[1]
        if date >= year:
            coauthor_count += count
    return coauthor_count


def get_interest_id(mentee_pub_years, mentor_pub_years):
    return set(
        [
            pubid_year[0]
            for pubid_year in list(
                set(mentee_pub_years).intersection(set(mentor_pub_years))
            )
        ]
    )


def get_copub_position(copubs_ids, mentee_position_year):
    list_positions = []
    for id_position in mentee_position_year:
        if id_position[0] in copubs_ids:
            list_positions.append(id_position[1])
    return np.array(list_positions).astype(np.int)


def make_df_table(df, table_name="temp_s2"):
    """
    Creates a table out of the pandas dataframe.
    """
    _load_dataframe_to_redshift(
        df, table_name, create_table=True, write_privileges=True
    )
    return None


def divide_zero(num, den):
    if num == 0 or den == 0:
        return 0
    else:
        return num / den


def candidate_selection(df):
    """
    This function will filter the pairs based on some condition
    :param df:
    :return:
    """
    # keeping pairs where
    # - mentee has pub start higher than candidate mentor
    # - OR mentee has dense pub start higher than dense candidate mentor
    # - count of pubs of mentor is higher than the mentee before copub
    df = df.query(
        "dense_mte_pub_start > dense_coa_pub_start or mte_pub_start > coa_pub_start"
    )
    return df[df["coa_pubs_before_copub"] >= df["mte_pubs_before_copub"]]


def get_count_to_date(list_pubs, end):
    """
    returns count of years less than end date
    """
    return np.sum(np.array(list_pubs) <= end)


def get_years(x):
    """
    takes in a list of tuples of (corpus_paper_id, year) and returns year
    :param x: list of tuples
    :return: list of years
    """
    list_data = []
    for i in x:
        list_data.append(int(i[1]))
    return list_data


def intersect(mentee_pub_years, mentor_pub_years):
    return get_years(list(set(mentee_pub_years).intersection(set(mentor_pub_years))))
