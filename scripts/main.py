import logging
from pathlib import Path

from sklearn.linear_model import LinearRegression

from clean_code.data.dishwasher import load_dishwasher_runs
from clean_code.data.key_tags import load_key_tags
from clean_code.data.recipes import load_recipes

from clean_code.logger import initialize_logging

DATA_DIR = Path('data')

_logger = logging.getLogger(__file__)


def main():
    initialize_logging()

    recipes = load_recipes(recipes_path=DATA_DIR / "lunch_recipes.csv")
    attendance = load_key_tags(key_tags_path=DATA_DIR / "key_tag_logs.csv")
    dishwasher_runs = load_dishwasher_runs(dishwasher_path=DATA_DIR / "dishwasher_log.csv")

    _logger.info("Merging data")
    df = recipes.merge(attendance,
                       on="date",
                       how="outer")
    df = df.merge(dishwasher_runs)

    _logger.info("Filling all missing values with 0")
    df = df.fillna(0)

    x = df.drop(["dishwashers", "date"], axis=1)
    y = df["dishwashers"]

    _logger.info("Fitting linear regression model")
    model = LinearRegression(fit_intercept=False, positive=True)
    model = model.fit(x, y)

    _logger.info("Model fitted")
    result = list(zip(model.feature_names_in_, model.coef_))

    # Sort the results
    result = sorted(result, key=lambda r: r[1], reverse=True)

    print("Coefficients of features in linear model:")
    for feature, coefficient in result:
        print(f"{feature}: {round(coefficient, 3)}")


if __name__ == "__main__":
    main()
