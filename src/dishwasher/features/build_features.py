import logging

import pandas as pd

LOGGER = logging.getLogger(__name__)


def get_all_features(recipes: pd.DataFrame, attendance: pd.DataFrame, dishwasher: pd.DataFrame) -> pd.DataFrame:
    """Build full feature set"""
    LOGGER.info("Building full feature set")
    return recipes \
        .merge(attendance, on="date", how="outer") \
        .merge(dishwasher) \
        .fillna(0)
