from typing import List, Dict
import os
import json
import openai
import pandas as pd
import singlestoredb as s2

from src.constants import DB_CONNECTION_URL, OPENAI_API_KEY
from src.utils import drop_table, get_models, get_model_embedding

db_connection = s2.connect(DB_CONNECTION_URL)
openai.api_key = OPENAI_API_KEY


def load_leaderboard_df():
    leaderboard_path = os.path.join('leaderboard/datasets/leaderboard.json')
    if os.path.exists(leaderboard_path):
        return pd.read_json(leaderboard_path, dtype={'still_on_hub': bool})
    else:
        print(f"The file '{leaderboard_path}' does not exists")


def load_model_embeddings_dataset() -> List[Dict[str, str]]:
    path = os.path.join('datasets/model_embeddings.json')
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    else:
        return []


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
                    readme LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
                )
            ''')

    def create_model_embeddings_table():
        with db_connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS model_embeddings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    embedding BLOB
                )
            ''')

    def create_models_twitter_posts_table():
        with db_connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS models_twitter_posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    embedding BLOB
                )
            ''')

    def create_models_reddit_posts_table():
        with db_connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS models_reddit_posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    embedding BLOB
                )
            ''')

    def create_models_github_repos_table():
        with db_connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS models_github_repos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    embedding BLOB
                )
            ''')

    create_models_table()
    create_model_embeddings_table()
    create_models_twitter_posts_table()
    create_models_reddit_posts_table()
    create_models_github_repos_table()


def fill_tables():
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM models')
        has_models = bool(cursor.fetchall()[0][0])

    def fill_models_table():
        if not has_models:
            with db_connection.cursor() as cursor:
                leaderboard_df = load_leaderboard_df()
                leaderboard_df.drop('created_at', axis=1, inplace=True)
                values = leaderboard_df.to_records(index=False).tolist()
                cursor.executemany(f'''
                    INSERT INTO models (name, author, repo_id, score, link, still_on_hub, arc, hellaswag, mmlu, truthfulqa, winogrande, gsm8k, readme, downloads, likes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', values)

    def fill_model_embeddings_table():
        with db_connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM model_embeddings')
            has_model_embeddings = bool(cursor.fetchall()[0][0])

            if not has_models or not has_model_embeddings:
                embeddings_dataset = load_model_embeddings_dataset()
                models = get_models(query='ORDER BY score DESC')[:5]
                values = []

                for model in models:
                    embedding = get_model_embedding(model, embeddings_dataset)
                    values.append([model['repo_id'], embedding[1], embedding[0]])

                if len(values) > len(embeddings_dataset):
                    df = pd.DataFrame(values, columns=['model_repo_id', 'text', 'embedding'])
                    df.to_json(os.path.abspath('datasets/model_embeddings.json'), orient='records')

                cursor.executemany(f'''
                    INSERT INTO model_embeddings (model_repo_id, text, embedding)
                    VALUES (%s, %s, JSON_ARRAY_PACK(%s))
                ''', [[value[0], value[1], str(value[2])] for value in values])

    fill_models_table()
    fill_model_embeddings_table()


# drop_table('models')
# drop_table('model_embeddings')
# drop_table('twitter_posts')
# drop_table('reddit_posts')
create_tables()
fill_tables()
