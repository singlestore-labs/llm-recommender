import os
import requests
from huggingface_hub import snapshot_download
from dotenv import load_dotenv
from datetime import datetime
from time import time

from src.display.utils import (
    BENCHMARK_COLS,
    COLS
)

from src.envs import EVAL_REQUESTS_PATH, EVAL_RESULTS_PATH, QUEUE_REPO, RESULTS_REPO, DATASETS_PATH
from src.populate import get_leaderboard_df
from src.tools.collections import update_collections

load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')


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


def get_hf_model_details(repo_id: str):
    request_url = f'https://huggingface.co/api/models/{repo_id}'
    response = requests.get(request_url, headers={'Authorization': f'Bearer {HF_TOKEN}'})

    if response.status_code == 200:
        data = response.json()
        return {
            'downloads': data.get('downloads', 0),
            'likes': data.get('likes', 0),
            'created_at': data.get('createdAt')
        }
    else:
        return {
            'downloads': 0,
            'likes': 0,
            'created_at': ''
        }


def get_hf_model_readme(repo_id: str):
    request_url = f'https://huggingface.co/{repo_id}/raw/main/README.md'
    response = requests.get(request_url)

    if response.status_code == 200:
        return response.text
    else:
        return ''


def create_dataset():
    raw_df = get_leaderboard_df(EVAL_RESULTS_PATH, EVAL_REQUESTS_PATH, COLS, BENCHMARK_COLS)
    update_collections(raw_df.copy())

    df = (
        raw_df[raw_df['author'].notna()]
        [["model", "author", "model_name_for_query", "average", "link", "still_on_hub", 'arc', 'hellaswag', 'mmlu',
          'truthfulqa', 'winogrande', 'gsm8k',]]
        .rename(columns={"model": "name", "model_name_for_query": "repo_id", "average": "score"}))

    for i, row in df.iterrows():
        details = get_hf_model_details(row['repo_id'])
        readme = get_hf_model_readme(row['repo_id'])
        df.at[i, 'readme'] = readme
        df.at[i, 'downloads'] = details['downloads']
        df.at[i, 'likes'] = details['likes']
        df.at[i, 'created_at'] = datetime.fromisoformat(
            details['created_at'].replace("Z", "+00:00")
        ).timestamp() if details['created_at'] else time()

    df.to_json(f'{DATASETS_PATH}/leaderboard.json', orient='records')


download_results()
create_dataset()
