from huggingface_hub import snapshot_download

from src.display.utils import (
    BENCHMARK_COLS,
    COLS
)

from src.envs import EVAL_REQUESTS_PATH, EVAL_RESULTS_PATH, QUEUE_REPO,  RESULTS_REPO
from src.populate import get_leaderboard_df
from src.tools.collections import update_collections


def download_results():
    try:
        print(EVAL_REQUESTS_PATH)
        snapshot_download(
            repo_id=QUEUE_REPO, local_dir=EVAL_REQUESTS_PATH, repo_type="dataset", tqdm_class=None, etag_timeout=30
        )
    except Exception as e:
        print(e)

    try:
        print(EVAL_RESULTS_PATH)
        snapshot_download(
            repo_id=RESULTS_REPO, local_dir=EVAL_RESULTS_PATH, repo_type="dataset", tqdm_class=None, etag_timeout=30
        )
    except Exception as e:
        print(e)


def create_dataset():
    df = get_leaderboard_df(EVAL_RESULTS_PATH, EVAL_REQUESTS_PATH, COLS, BENCHMARK_COLS)
    update_collections(df.copy())
    df.to_json('leaderboard.json', orient='records')


# download_results()
create_dataset()
