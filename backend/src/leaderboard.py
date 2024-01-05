import os
import pandas as pd

from . import constants
from . import db
from . import ai
from . import utils


def get_df():
    leaderboard_path = os.path.join('leaderboard/datasets/leaderboard.json')

    if os.path.exists(leaderboard_path):
        df = pd.read_json(leaderboard_path, dtype={'still_on_hub': bool})
        # ! REMOVE .head(*)
        return df.head(10)
    else:
        print(f"The file '{leaderboard_path}' does not exists")


def get_models():
    existed_models_repo_ids = [record[0][0] for record in db.get_models('repo_id', as_dict=False)]
    leaderboard_df = get_df()

    for index, row in leaderboard_df.iterrows():
        print(index, row)

    return []


def insert_models(models):
    return []
