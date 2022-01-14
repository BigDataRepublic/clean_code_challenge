import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

LOGGER = logging.getLogger(__name__)


def read_attendance_logs(path: Path) -> pd.DataFrame:
    LOGGER.info("Reading key tag logs.")
    return pd.read_csv(path)


def _parse_time_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    LOGGER.info("Parsing time columns from attendance list.")
    dataframe["timestamp"] = dataframe.timestamp.apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    )
    dataframe["date"] = dataframe["timestamp"].values.astype(dtype='datetime64[ms]')

    return dataframe


def preprocess_attendance(key_tag_logs: pd.DataFrame) -> pd.DataFrame:
    LOGGER.info("Preprocessing attendance list.")
    key_tag_logs[["timestamp", "date"]] = _parse_time_columns(
        key_tag_logs[["timestamp"]].copy()
    )

    LOGGER.info("Determining lunch dates per person.")

    preprocessed = key_tag_logs[["name", "date", "event"]] \
        .groupby(["name", "date"]).agg(["count"]) \
        .unstack() \
        .T \
        .reset_index() \
        .drop(["level_0", "level_1"], axis=1)
    name_columns = [c for c in preprocessed.columns if c != "date"]
    preprocessed[name_columns] = preprocessed[name_columns].applymap(lambda x: 1. if x > 0 else 0.)

    return preprocessed
