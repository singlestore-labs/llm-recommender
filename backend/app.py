import os
import requests
import singlestoredb as s2
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')
DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')
DB_NAME = os.environ.get('DB_NAME')

db_connection = s2.connect(DB_CONNECTION_URL)


def load_leaderboard_df():
    leaderboard_path = os.path.join('leaderboard/datasets/leaderboard.json')

    if os.path.exists(leaderboard_path):
        return pd.read_json(leaderboard_path, dtype={'still_on_hub': bool})
    else:
        print(f"The file '{leaderboard_path}' does not exists")


def drop_table(table_name: str):
    with db_connection.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {DB_NAME}.{table_name}')


def create_models_table():
    with db_connection.cursor() as cursor:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS models (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(512) NOT NULL,
                author VARCHAR(512) NOT NULL,
                repo_id VARCHAR(1024) NOT NULL,
                score DECIMAL(5, 2) NOT NULL,
                link VARCHAR(255) NOT NULL,
                still_on_hub BOOLEAN NOT NULL,
                downloads INT,
                likes INT,
                readme TEXT
            )
        ''')


def fill_models_table():
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM models')
        has_records = bool(cursor.fetchall()[0][0])

        if not has_records:
            leaderboard_df = load_leaderboard_df()
            values = leaderboard_df.to_records(index=True).tolist()

            cursor.executemany(f'''
                INSERT INTO models (id, name, author, repo_id, score, link, still_on_hub)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', values)


def get_models(select='*'):
    with db_connection.cursor() as cursor:
        cursor.execute(f'SELECT {select} FROM models')
        return cursor.fetchall()


def get_models_repo_id_df():
    repo_ids = [i[0] for i in get_models('repo_id')]
    return pd.DataFrame({'repo_id': repo_ids})


def init_database():
    # drop_table('models')
    create_models_table()
    fill_models_table()


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
        return None


def get_hf_model_readme(repo_id: str):
    request_url = f'https://huggingface.co/{repo_id}/raw/main/README.md'
    response = requests.get(request_url)

    if response.status_code == 200:
        return response.text
    else:
        return None


def update_models():
    df = get_models_repo_id_df()

    for i, row in df.iterrows():
        details = get_hf_model_details(row['repo_id'])
