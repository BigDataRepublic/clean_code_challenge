from typing import List, Callable
from datetime import datetime, time

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import os
from clean_code_challenge.io import (
    read_recipes,
    read_attendance_sheet,
    read_diswasher_log,
)
from clean_code_challenge.config import get_data_path_resolver


def train_model() -> dict:
    """
    Train a linear regression on the data and return the coefficients
    """
    data_path_resolver = get_data_path_resolver()
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
