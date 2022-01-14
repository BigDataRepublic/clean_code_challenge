from datetime import time
from typing import List, Optional

import pandas as pd
from sklearn.linear_model import LinearRegression


def read_data(path: str, cols: Optional[List[str]]) -> pd.DataFrame:
    """
    :param path: local path of the file to read
    :param cols: cols to keep, use None for all
    :return: the file as pandas DataFrame
    """
    df = pd.read_csv(path, usecols=cols)
    return df


def clean_recipes(df: pd.DataFrame, supply_words: List[str]) -> pd.DataFrame:
    """
    :param supply_words: a list of words to check on
    :param df: the recipe DataFrame
    :return: a DataFrame with a boolean value per recipe and supply words
    """
    for word in supply_words:
        df[word] = (
            df["recipe"]
                .str.lower()
                .str.contains(pat=r"\b{}\b".format(word), regex=True)
        )
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.drop("recipe", axis=1)
    return df


def clean_attendance_sheet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the attendance log to check who had lunch in the office on a certain day
    :param df: DataFrame containing the attendance log
    :return: a DataFrame with dates and all employees lunch information
    """
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    df["time"] = pd.to_datetime(df["timestamp"]).dt.time
    dates = df["date"].unique()
    names = df["name"].unique()
    lunch_df = pd.DataFrame(columns=names)
    lunch_df["date"] = dates
    lunch_df.index = lunch_df["date"]
    lunch_df = lunch_df.fillna(0)
    for i, row in df.loc[df["time"] < time(12, 0, 0)].iterrows():
        if row["event"] == "check in":
            lunch_df.at[row["date"], row["name"]] = 1
        elif row["event"] == "check out":
            lunch_df.at[row["date"], row["name"]] = 0
    lunch_df = lunch_df.reset_index(drop=True)
    return lunch_df


def clean_dishwasher_runs(df: pd.DataFrame) -> pd.DataFrame:
    """
    :param df: dishwasher DataFrame
    :return: dishwasher DataFrame with parsed date
    """
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def train_model(train_set: pd.DataFrame) -> dict:
    """
    Train a linear regression on the dishwasher dataset
    :param train_set: the features and targets of the dishwasher data
    :return: coefficients of the features
    """
    targets = train_set["dishwashers"]
    train_set = train_set.drop(["dishwashers", "date"], axis=1)
    lin_reg = LinearRegression(fit_intercept=False, positive=True).fit(
        train_set, targets
    )
    return dict(zip(lin_reg.feature_names_in_, [round(c, 3) for c in lin_reg.coef_]))


if __name__ == "__main__":
    recipes = read_data("data/lunch_recipes.csv", ["recipe", "date"])
    recipes = clean_recipes(recipes, supply_words=["pan", "rasp", "kom"])
    attendance_sheet = read_data("data/key_tag_logs.csv", None)
    attendance_sheet = clean_attendance_sheet(attendance_sheet)
    dishwasher_runs = read_data("data/dishwasher_log.csv", None)
    dishwasher_runs = clean_dishwasher_runs(dishwasher_runs)
    data_set = (
        recipes.merge(attendance_sheet, on="date", how="outer")
            .merge(dishwasher_runs)
            .fillna(0)
    )
    results = train_model(data_set)
    print(results)
