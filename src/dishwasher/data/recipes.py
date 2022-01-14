import logging
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
LOGGER = logging.getLogger(__name__)


def read_recipe_logs(path: Path) -> pd.DataFrame:
    LOGGER.info("Reading recipe logs")
    return pd.read_csv(path)


def preprocess_recipes(recipe_logs: pd.DataFrame) -> pd.DataFrame:
    """Preprocess recipes file."""
    supply_words = ["pan", "rasp", "kom"]

    for word in supply_words:
        recipe_logs[word] = recipe_logs.recipe.apply(lambda text: _clean_text(text).count(word) > 0)
        recipe_logs[word] = recipe_logs[word].apply(lambda x: bool(x))

    recipe_logs["date"] = recipe_logs.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    return recipe_logs.drop(["servings", "recipe", "url", "dish"], axis=1)


def _clean_text(text: str) -> List[str]:
    """Clean text by separating all the words and removing punctuation"""
    return ["".join(c for c in word if c.isalnum()).lower() for word in text.split()]
