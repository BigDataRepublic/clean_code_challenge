import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

LOGGER = logging.getLogger(__name__)


def read_dishwasher_logs(path: Path) -> pd.DataFrame:
    LOGGER.info("Reading dishwasher logs")
    dataframe = pd.read_csv(path)
    dataframe["date"] = dataframe.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))

    return dataframe
