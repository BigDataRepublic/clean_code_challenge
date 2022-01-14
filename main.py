from datetime import datetime, time, date
from os import path
from typing import List

import pandas as pd
from sklearn.linear_model import LinearRegression

extra_dishes_contributing_ingredients = ["pan", "rasp", "kom"]


class DishWasher:
    def __init__(self):
        self.lunch_time = time(hour=12, minute=0, second=0)
        self.check_out_event = "check out"
        self.check_in_event = "check in"

    def _remove_punctuation(self, text: str) -> str:
        return "".join(character for character in text if character.isalnum())

    def _extract_words_from_recipe(self, text: str) -> List[str]:
        lowercase_text = text.lower()
        lowercase_cleaned_text = self._remove_punctuation(lowercase_text)
        lowercase_cleaned_words = lowercase_cleaned_text.split()
        return lowercase_cleaned_words

    def _contains_ingredient(self, text: str, ingredient: str) -> bool:
        return self._extract_words_from_recipe(text).count(ingredient) > 0

    def _load_recipes(self) -> pd.DataFrame:
        script_path = path.dirname(path.abspath(__file__))
        file_path = path.join(script_path, "data/lunch_recipes.csv")
        lunch_recipes = pd.read_csv(file_path)
        return lunch_recipes

    def _check_ingredients_in_recipes(
        self, lunch_recipes: pd.DataFrame
    ) -> pd.DataFrame:
        for ingredient in extra_dishes_contributing_ingredients:
            lunch_recipes[f"{ingredient}"] = lunch_recipes.recipe.apply(
                self._contains_ingredient, ingredient=ingredient
            )
        columns_to_remove = ["servings", "recipe", "url", "dish"]
        lunch_recipes.drop(columns=columns_to_remove, inplace=True)
        lunch_recipes["date"] = pd.to_datetime(lunch_recipes["date"])
        return lunch_recipes

    def _load_key_tag_logs(
        self,
    ) -> pd.DataFrame:
        script_path = path.dirname(path.abspath(__file__))
        file_path = path.join(script_path, "data/key_tag_logs.csv")
        key_tag_logs = pd.read_csv(file_path)
        return key_tag_logs

    def _was_present_at_lunch(
        self, name: str, lunch_date: date, key_tag_logs: pd.DataFrame
    ) -> bool:
        person_key_tag_entries = key_tag_logs[key_tag_logs.name == name]
        person_key_tag_entries = person_key_tag_entries[
            person_key_tag_entries["datetime"].dt.date == lunch_date
        ]
        person_check_ins_before_lunch = person_key_tag_entries[
            (person_key_tag_entries["event"] == self.check_in_event)
            & (person_key_tag_entries["datetime"].dt.time < self.lunch_time)
        ]
        person_check_outs_after_lunch = person_key_tag_entries[
            (person_key_tag_entries["event"] == self.check_out_event)
            & (person_key_tag_entries["datetime"].dt.time < self.lunch_time)
        ]
        was_present_at_lunch = (
            person_check_ins_before_lunch.shape[0] > 0
            and person_check_outs_after_lunch.shape[0] > 0
        )
        return was_present_at_lunch

    def _create_attendance_sheet(
        self,
    ):
        key_tag_logs = self._load_key_tag_logs()
        key_tag_logs["datetime"] = pd.to_datetime(key_tag_logs["timestamp"])
        unique_key_tag_log_dates = key_tag_logs["datetime"].dt.date.unique()
        attendance_sheet = pd.DataFrame(
            data=pd.to_datetime(unique_key_tag_log_dates), columns=["date"]
        )

        for name in key_tag_logs.name.unique():
            dates_present_for_lunch = []
            for log_date in unique_key_tag_log_dates:
                if self._was_present_at_lunch(
                    name=name, lunch_date=log_date, key_tag_logs=key_tag_logs
                ):
                    dates_present_for_lunch.append(log_date)

            attendance_sheet[f"{name}"] = attendance_sheet["date"].apply(
                lambda x: 1 if x in list(dates_present_for_lunch) else 0
            )

        return attendance_sheet

    def _get_lunch_ingredients(self):
        lunch_recipes = self._load_recipes()
        return self._check_ingredients_in_recipes(lunch_recipes=lunch_recipes)

    def _load_dishwasher_log(self):
        script_path = path.dirname(path.abspath(__file__))
        file_path = path.join(script_path, "data/dishwasher_log.csv")
        dishwasher_log = pd.read_csv(file_path)
        dishwasher_log["date"] = dishwasher_log.date.apply(
            lambda x: datetime.strptime(x, "%Y-%m-%d")
        )
        return dishwasher_log

    def train_model(self):
        lunch_ingredients = self._get_lunch_ingredients()
        attendance_sheet = self._create_attendance_sheet()
        dishwasher_log = self._load_dishwasher_log()
        default_value = 0

        merged_logs = (
            lunch_ingredients.merge(right=attendance_sheet, on="date", how="outer")
            .merge(right=dishwasher_log, how="inner")
            .fillna(value=default_value)
        )
        X = merged_logs.drop(columns=["dishwashers", "date"])
        y = merged_logs["dishwashers"]
        regressor = LinearRegression(fit_intercept=False, positive=True)
        fitted_regression = regressor.fit(X=X, y=y)
        return dict(
            zip(
                fitted_regression.feature_names_in_,
                [round(c, 3) for c in fitted_regression.coef_],
            )
        )


if __name__ == "__main__":
    dishwasher = DishWasher()
    print(dishwasher.train_model())
