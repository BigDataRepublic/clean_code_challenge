import argparse
import logging

import coloredlogs  # type: ignore

from dishwasher.data.attendance import read_attendance_logs, preprocess_attendance
from dishwasher.data.dishwasher import read_dishwasher_logs
from dishwasher.data.recipes import read_recipe_logs, preprocess_recipes
from dishwasher.features.build_features import get_all_features
from dishwasher.model.train import train_model

LOGGER = logging.getLogger(__name__)

coloredlogs.install(level=logging.INFO)


def main():
    argument_parser = argparse.ArgumentParser(
        description="Model that predicts the number of times the dishwasher has to run on a particular day at the office."
    )
    argument_parser.add_argument(
        "-d",
        "--data-dishwasher",
        dest="dishwasher",
        help="Dishwasher logs",
        default="./data/dishwasher_log.csv",
    )
    argument_parser.add_argument(
        "-k", "--data-key-tag", dest="key_tag", help="Key tag logs", default="./data/key_tag_logs.csv"
    )
    argument_parser.add_argument(
        "-l",
        "--data-recipes",
        dest="recipes",
        help="Lunch recipe logs",
        default="./data/lunch_recipes.csv",
    )
    argument_parser.add_argument(
        "-m",
        "--mode",
        choices=["train"],
        help="Model mode",
        default="train",
    )

    arguments, _ = argument_parser.parse_known_args()

    if arguments.mode == "train":
        attendance_logs = read_attendance_logs(arguments.key_tag)
        dishwasher_logs = read_dishwasher_logs(arguments.dishwasher)
        recipes = read_recipe_logs(arguments.recipes)

        features = get_all_features(
            attendance=preprocess_attendance(attendance_logs),
            dishwasher=dishwasher_logs,
            recipes=preprocess_recipes(recipes),
        )

        train_model(features)
    else:
        raise NotImplementedError(
            f"Mode {arguments.mode} has not yet been implemented."
        )


if __name__ == "__main__":
    main()
