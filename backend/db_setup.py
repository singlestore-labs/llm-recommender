import os
import json
import openai
import time
from datetime import datetime
import pandas as pd

from src.constants import OPENAI_API_KEY, TOKENS_TRASHHOLD_LIMIT
from src.db import db_connection
from src.utils import drop_table, create_embeddings, count_tokens, string_into_chunks, clean_string

openai.api_key = OPENAI_API_KEY


def load_leaderboard_df():
    leaderboard_path = os.path.join('leaderboard/datasets/leaderboard.json')

    if os.path.exists(leaderboard_path):
        df = pd.read_json(leaderboard_path, dtype={'still_on_hub': bool})
        df['created_at'] = df['created_at'].apply(
            lambda created_at: datetime.fromisoformat(
                created_at.replace("Z", "+00:00")
            ).timestamp() if created_at else time.time()
        )

        # ! REMOVE .head(*)
        return df.head(25)
    else:
        print(f"The file '{leaderboard_path}' does not exists")


def create_tables():
    def create_models_table():
        with db_connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS models (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(512) NOT NULL,
                    author VARCHAR(512) NOT NULL,
                    repo_id VARCHAR(1024) NOT NULL,
                    score DECIMAL(5, 2) NOT NULL,
                    arc DECIMAL(5, 2) NOT NULL,
                    hellaswag DECIMAL(5, 2) NOT NULL,
                    mmlu DECIMAL(5, 2) NOT NULL,
                    truthfulqa DECIMAL(5, 2) NOT NULL,
                    winogrande DECIMAL(5, 2) NOT NULL,
                    gsm8k DECIMAL(5, 2) NOT NULL,
                    link VARCHAR(255) NOT NULL,
                    downloads INT,
                    likes INT,
                    still_on_hub BOOLEAN NOT NULL,
                    created_at TIMESTAMP,
                    embedding BLOB
                )
            ''')

    def create_model_readmes_table():
        with db_connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS model_readmes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    clean_text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    embedding BLOB
                )
            ''')

    def create_model_twitter_posts_table():
        with db_connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS model_twitter_posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    clean_text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    embedding BLOB
                )
            ''')

    def create_model_reddit_posts_table():
        with db_connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS model_reddit_posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    post_id VARCHAR(256),
                    title VARCHAR(512),
                    clean_text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    link VARCHAR(256),
                    created_at TIMESTAMP,
                    embedding BLOB
                )
            ''')

    def create_model_github_repos_table():
        with db_connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS model_github_repos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    repo_id INT,
                    name VARCHAR(512),
                    description TEXT,
                    clean_readme LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    link VARCHAR(256),
                    created_at TIMESTAMP,
                    embedding BLOB
                )
            ''')

    create_models_table()
    create_model_readmes_table()
    create_model_twitter_posts_table()
    create_model_reddit_posts_table()
    create_model_github_repos_table()


def fill_tables():
    leaderboard_df = load_leaderboard_df()

    with db_connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM models')
        has_models = bool(cursor.fetchall()[0][0])

    def fill_models_table():
        if not has_models:
            with db_connection.cursor() as cursor:
                df = leaderboard_df.copy()
                df.drop('readme', axis=1, inplace=True)
                df['embeddig'] = [str(create_embeddings(json.dumps(record))[0]) for record in df.to_dict('records')]
                values = df.to_records(index=False).tolist()
                cursor.executemany(f'''
                    INSERT INTO models (name, author, repo_id, score, link, still_on_hub, arc, hellaswag, mmlu, truthfulqa, winogrande, gsm8k, downloads, likes, created_at, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), JSON_ARRAY_PACK(%s))
                ''', values)

    def fill_model_reamdes_table():
        with db_connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM model_readmes')
            has_model_readmes = bool(cursor.fetchall()[0][0])

            if not has_models or not has_model_readmes:
                df = leaderboard_df.copy()[['repo_id', 'readme']]
                df = df.rename(columns={'repo_id': 'model_repo_id', 'readme': 'text'})

                for index, row in df.iterrows():
                    text = row['text']

                    if count_tokens(text) <= TOKENS_TRASHHOLD_LIMIT:
                        continue

                    for chunk_index, chunk in enumerate(string_into_chunks(text)):
                        if chunk_index == 0:
                            df.at[index, 'text'] = chunk
                        else:
                            df = pd.concat([df, pd.DataFrame([{**row, 'text': chunk}])], ignore_index=True)

                df['clean_text'] = [clean_string(row['text']) for i, row in df.iterrows()]
                df['embedding'] = [str(create_embeddings(json.dumps({
                    'model_repo_id': row['model_repo_id'],
                    'clean_text': row['clean_text']
                }))[0]) for i, row in df.iterrows()]
                values = df.to_records(index=False).tolist()

                cursor.executemany(f'''
                    INSERT INTO model_readmes (model_repo_id, text, clean_text, embedding)
                    VALUES (%s, %s, %s, JSON_ARRAY_PACK(%s))
                ''', values)

    fill_models_table()
    fill_model_reamdes_table()


# drop_table('models')
# drop_table('model_readmes')
# drop_table('model_twitter_posts')
# drop_table('model_reddit_posts')
# drop_table('model_github_repos')
create_tables()
fill_tables()
