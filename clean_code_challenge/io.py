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
    recipes = pd.read_csv(data_path_resolver("lunch_recipes.csv"))
    for word in supply_words:
        recipes[word] = recipes.recipe.apply(lambda text: text.contains(word))
        recipes[word] = recipes[word].apply(lambda x: x is True)
    recipes["date"] = recipes.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    recipes = recipes.drop(["servings", "recipe", "url", "dish"], axis=1)

    return recipes


def read_attendance_sheet(data_path_resolver: Callable[[str], str]) -> pd.DataFrame:
    """
    Read key tag log to infer attendance sheet
    """
    key_tag_logs = pd.read_csv(data_path_resolver("key_tag_logs.csv"))
    key_tag_logs["timestamp"] = key_tag_logs.timestamp.apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    )
    key_tag_logs["date"] = key_tag_logs.timestamp.apply(
        lambda x: datetime.strptime(x[:10], "%Y-%m-%d")
    )
    key_tag_logs["time"] = key_tag_logs.timestamp.apply(lambda x: x.time())

    attendance_sheet = pd.DataFrame(
        np.array(key_tag_logs.date), columns=["date"]
    ).drop_duplicates()

    for name in key_tag_logs.name.unique():
        lunch_dates = []
        for date in key_tag_logs.date.unique():
            personal_day_log = key_tag_logs[key_tag_logs.name == name]
            personal_day_log = personal_day_log[personal_day_log.date == date]

            check_in_events = personal_day_log[personal_day_log.event == "check in"]
            check_in_events = check_in_events[check_in_events.time < time(12, 0, 0)]

            check_out_events = personal_day_log[personal_day_log.event == "check out"]
            check_out_events = check_out_events[check_out_events.time > time(12, 0, 0)]
            if check_out_events.shape[0] > 0 and check_in_events.shape[0] > 0:
                lunch_dates.append(date)

        attendance_sheet[name] = attendance_sheet.date.apply(
            lambda x: 1 if x in list(lunch_dates) else 0
        )
    return attendance_sheet


def read_diswasher_log(data_path_resolver: Callable[[str], str]) -> pd.DataFrame:
    """
    Read dishwasher log into a clean dataframe
    """
    dishwasher_log = pd.read_csv(data_path_resolver("dishwasher_log.csv"))
    dishwasher_log["date"] = dishwasher_log.date.apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d")
    )
    return dishwasher_log
