from typing import List, Dict
import json
import openai
import tiktoken
import numpy as np
import singlestoredb as s2
from decimal import Decimal


from .constants import DB_CONNECTION_URL, DB_NAME, OPENAI_API_KEY

db_connection = s2.connect(DB_CONNECTION_URL)
openai.api_key = OPENAI_API_KEY


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def string_into_chunks(string: str, max_length=5000):
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


def create_embeddings(input):
    data = openai.embeddings.create(input=input, model='text-embedding-ada-002').data
    return [i.embedding for i in data]


def create_avg_embeddings(input: str):
    tokens = count_tokens(input)

    if (tokens <= 2047):
        return create_embeddings(input)[0]

    chunks = string_into_chunks(input)
    embeddings = create_embeddings(chunks)
    return np.mean(np.array(embeddings), axis=0).tolist()


def get_model_embedding(model, model_embeddings: List[Dict[str, str]] = []):
    for item in model_embeddings:
        if item['model_repo_id'] == model['repo_id'] and item['embedding']:
            return item['embedding'], item['text']

    model_json = json.dumps(model, cls=DecimalEncoder)

    return create_avg_embeddings(model_json), model_json


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
