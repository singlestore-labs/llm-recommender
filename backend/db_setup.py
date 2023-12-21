import os
import json
import openai
from typing import List, Dict
import numpy as np
import pandas as pd
import singlestoredb as s2
import tiktoken
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')
DB_NAME = os.environ.get('DB_NAME')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
HF_TOKEN = os.getenv('HF_TOKEN')

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


def string_into_chunks(string: str, max_length=2048):
    if len(string) <= max_length:
        return [string]

    delimiter = ' '
    words = string.split(delimiter)
    chunks = []
    current_chunk = []

    for word in words:
        if len(delimiter.join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(delimiter.join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(delimiter.join(current_chunk))

    return chunks


def count_tokens(text: str):
    enc = tiktoken.get_encoding('cl100k_base')
    return len(enc.encode(text))


def create_embedding(input):
    data = openai.embeddings.create(input=input, model='text-embedding-ada-002').data
    return [i.embedding for i in data]


def create_avg_embeddings(input: str):
    tokens = count_tokens(input)

    if (tokens <= 2047):
        return create_embedding(input)[0]

    chunks = string_into_chunks(input, 2047)
    embeddings = create_embedding(chunks)
    return np.mean(np.array(embeddings), axis=0).tolist()


def get_model_embedding(model, model_embeddings: List[Dict[str, str]] = []):
    for item in model_embeddings:
        if item['model_repo_id'] == model['repo_id'] and item['embedding']:
            return item['embedding']

    return create_avg_embeddings(str(model))


def get_models(select='*', query='', as_dict=True):
    with db_connection.cursor() as cursor:
        _query = f'SELECT {select} FROM models'

        if query:
            _query += f' {query}'

        cursor.execute(_query)

        if as_dict:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        return cursor.fetchall()


def drop_table(table_name: str):
    with db_connection.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {DB_NAME}.{table_name}')


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
                    embedding BLOB
                )
            ''')

    create_models_table()
    create_model_embeddings_table()


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
                models = get_models(query='ORDER BY score DESC')[:12]
                values = []

                for model in models:
                    values.append([model['repo_id'], get_model_embedding(model, embeddings_dataset)])

                df = pd.DataFrame(values, columns=['model_repo_id', 'embedding'])
                df.to_json(os.path.abspath('datasets/model_embeddings.json'), orient='records')

                cursor.executemany(f'''
                    INSERT INTO model_embeddings (model_repo_id, embedding)
                    VALUES (%s, JSON_ARRAY_PACK(%s))
                ''', [[value[0], str(value[1])] for value in values])

    fill_models_table()
    fill_model_embeddings_table()


# drop_table('models')
# drop_table('model_embeddings')
create_tables()
fill_tables()
