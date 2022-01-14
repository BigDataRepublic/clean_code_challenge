import logging
from typing import Any, Dict

import pandas as pd
from sklearn.linear_model import LinearRegression

LOGGER = logging.getLogger(__name__)


def train_model(features: pd.DataFrame) -> Dict[str, Any]:
    """
    Train dishwasher model.
    :param features: Feature set
    :return: Dictionary with model properties
    """
    LOGGER.info("Training model")
    reg = LinearRegression(fit_intercept=False, positive=True).fit(
        features.drop(["dishwashers", "date"], axis=1), features["dishwashers"]
    )
    return dict(zip(reg.feature_names_in_, [round(c, 3) for c in reg.coef_]))
