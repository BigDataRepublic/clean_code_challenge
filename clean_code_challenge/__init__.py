from typing import List, Callable
from datetime import datetime, time

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import os

SUPPLY_WORDS = ["pan", "rasp", "kom"]


def get_data_path(project_data_path: str) -> Callable[[str], str]:
    """
    Return a method that allows for resolving a full data path given a filename
    """

    def _get_data_path(filename: str) -> str:
        return os.path.join("data", filename)

    return _get_data_path


def remove_punctuation(text: str) -> List[str]:
    """
    Cleans text by seperating all the words and removing punctuation
    """
    str_list = [
        "".join(character for character in chunk if character.isalnum())
        for chunk in text.split()
    ]
    str_list = [str.lower() for str in str_list]
    return str_list


def read_recipes(data_path_resolver: Callable[[str], str]) -> pd.DataFrame:
    df = pd.read_csv(
        data_path_resolver("lunch_recipes.csv")
    )  # Read lunch recipes dataframe.
    for word in SUPPLY_WORDS:
        df[word] = df.recipe.apply(
            lambda text: remove_punctuation(text).count(word) > 0
        )  # count the amount of times a word occurs in the recipe.
        df[f"{word}"] = df[f"{word}"].apply(lambda x: x is True)
    df = df.drop("servings", axis=1)
    df = df.drop("recipe", axis=1)
    df["date"] = df.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    df = df.drop("url", axis=1)
    df = df.drop("dish", axis=1)

    return df


def read_attendance_sheet(data_path_resolver: Callable[[str], str]):
    df = pd.read_csv(data_path_resolver("key_tag_logs.csv"))
    df["timestamp2"] = df.timestamp.apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    )
    df["date"] = df.timestamp.apply(lambda x: datetime.strptime(x[:10], "%Y-%m-%d"))
    df["time"] = df.timestamp2.apply(lambda x: x.time())
    df["timestamp"] = df["timestamp2"]
    df = df.drop("timestamp2", axis=1)

    result = pd.DataFrame(np.array(df.date), columns=["date"]).drop_duplicates()

    # print(df.name.unique())
    for name in df.name.unique():
        lunchdates = []
        for datum in df.date.unique():
            df2 = df[df.name == name]
            df2 = df2[df2.date == datum]

            dataframe_check_in = df2[df2.event == "check in"]
            dataframe_check_in = dataframe_check_in[
                dataframe_check_in.time < time(12, 0, 0)
            ]

            df_check_out = df2[df2.event == "check out"]
            df_check_out = df_check_out[df_check_out.time > time(12, 0, 0)]
            if df_check_out.shape[0] > 0 and dataframe_check_in.shape[0] > 0:
                lunchdates.append(datum)

        result[f"{name}"] = result.date.apply(
            lambda x: 1 if x in list(lunchdates) else 0
        )

    result["date"] = result["date"]  # .apply(str)
    return result


def read_diswasher_log(data_path_resolver: Callable[[str], str]) -> pd.DataFrame:
    dishwasher_log = pd.read_csv(data_path_resolver("dishwasher_log.csv"))
    dishwasher_log["date"] = dishwasher_log.date.apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d")
    )
    return dishwasher_log


def train_model(alpha=0.1):
    data_path_resolver = get_data_path("data")
    recipes = read_recipes(data_path_resolver)
    attendance = read_attendance_sheet(data_path_resolver)
    dishwasher_log = read_diswasher_log(data_path_resolver)

    df = (
        recipes.merge(attendance, on="date", how="outer")
        .merge(dishwasher_log)
        .fillna(0)
    )
    reg = LinearRegression(fit_intercept=False, positive=True).fit(
        df.drop(["dishwashers", "date"], axis=1), df["dishwashers"]
    )
    return dict(zip(reg.feature_names_in_, [round(c, 3) for c in reg.coef_]))
