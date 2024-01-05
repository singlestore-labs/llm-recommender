
import os
import pandas as pd
from datetime import datetime
from time import time


def get_leaderboard_df():
    leaderboard_path = os.path.join('leaderboard/datasets/leaderboard.json')

    if os.path.exists(leaderboard_path):
        df = pd.read_json(leaderboard_path, dtype={'still_on_hub': bool})
        df['created_at'] = df['created_at'].apply(
            lambda created_at: datetime.fromisoformat(
                created_at.replace("Z", "+00:00")
            ).timestamp() if created_at else time()
        )

        # ! REMOVE .head(*)
        return df.head(10)
    else:
        print(f"The file '{leaderboard_path}' does not exists")


def get_models():
    existed_models = get_models
    leaderboard_df = get_leaderboard_df()
    return []


def insert_models(models):
    return []
