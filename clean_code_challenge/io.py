from typing import List, Callable
from datetime import datetime, time

import pandas as pd
import numpy as np
import os
from clean_code_challenge.util import remove_punctuation


def read_recipes(data_path_resolver: Callable[[str], str]) -> pd.DataFrame:
    """
    Read recipes from disk into a clean dataframe
    """
    supply_words = ["pan", "rasp", "kom"]
    df = pd.read_csv(data_path_resolver("lunch_recipes.csv"))
    for word in supply_words:
        df[word] = df.recipe.apply(
            lambda text: remove_punctuation(text).count(word) > 0
        )
        df[f"{word}"] = df[f"{word}"].apply(lambda x: x is True)
    df["date"] = df.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    df = df.drop(["servings", "recipe", "url", "dish"], axis=1)

    return df


def read_attendance_sheet(data_path_resolver: Callable[[str], str]) -> pd.DataFrame:
    """
    Read attendance sheet into a clean dataframe
    """
    df = pd.read_csv(data_path_resolver("key_tag_logs.csv"))
    df["timestamp2"] = df.timestamp.apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    )
    df["date"] = df.timestamp.apply(lambda x: datetime.strptime(x[:10], "%Y-%m-%d"))
    df["time"] = df.timestamp2.apply(lambda x: x.time())
    df["timestamp"] = df["timestamp2"]
    df = df.drop("timestamp2", axis=1)

    result = pd.DataFrame(np.array(df.date), columns=["date"]).drop_duplicates()

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
    return result


def read_diswasher_log(data_path_resolver: Callable[[str], str]) -> pd.DataFrame:
    """
    Read dishwasher log into a clean dataframe
    """
    dishwasher_log = pd.read_csv(data_path_resolver("dishwasher_log.csv"))
    dishwasher_log["date"] = dishwasher_log.date.apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d")
    )
    return dishwasher_log
