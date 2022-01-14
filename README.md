## Getting started
```bash
pip install -U .
```

## Usage
```text
$ dishwasher --help
usage: dishwasher [-h] [-d DISHWASHER] [-k KEY_TAG] [-l RECIPES] [-m {train}]

Model that predicts the number of times the dishwasher has to run on a particular day at the office.

optional arguments:
  -h, --help            show this help message and exit
  -d DISHWASHER, --data-dishwasher DISHWASHER
                        Dishwasher logs
  -k KEY_TAG, --data-key-tag KEY_TAG
                        Key tag logs
  -l RECIPES, --data-recipes RECIPES
                        Lunch recipe logs
  -m {train}, --mode {train}
                        Model mode
```
