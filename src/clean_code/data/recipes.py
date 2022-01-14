from datetime import datetime
import logging
import pandas as pd

_logger = logging.getLogger(__name__)

SUPPLY_WORDS = ["pan", "rasp", "kom"]


def clean(text):
    # This function cleans text by separating all the words and removing punctuation
    str_list = [''.join(char for char in s if char.isalnum())
                for s in text.split()]
    str_list = [s.lower() for s in str_list]
    return str_list


def load_recipes(recipes_path):
    _logger.info("Loading recipes")
    df = pd.read_csv(recipes_path)

    for wrd in SUPPLY_WORDS:
        # count the number of times a word occurs in the recipe.
        df[f"count_{wrd}"] = df.recipe.apply(
            lambda text: clean(text).count(wrd) > 0
        )
        df[f"count_{wrd}"] = df[f"count_{wrd}"].apply(lambda x: x is True)

    df = df.drop('servings', axis=1)
    df = df.drop('recipe', axis=1)
    df = df.drop("url", axis=1)
    df = df.drop("dish", axis=1)

    df['date'] = df.date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    _logger.debug("Recipes loaded")
    return df
