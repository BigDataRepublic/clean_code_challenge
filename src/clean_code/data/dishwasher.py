from datetime import datetime
import logging
import pandas as pd

_logger = logging.getLogger(__name__)


def load_dishwasher_runs(dishwasher_path):
    _logger.info("Loading dishwasher runs")
    runs = pd.read_csv(dishwasher_path)
    runs["date"] = runs.date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    _logger.debug("Dishwasher runs loaded")
    return runs
