import os
import openai
import numpy as np
import singlestoredb as s2
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')
DB_NAME = os.environ.get('DB_NAME')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
HF_TOKEN = os.getenv('HF_TOKEN')

db_connection = s2.connect(DB_CONNECTION_URL)
openai.api_key = OPENAI_API_KEY


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


def create_embeddings(input):
    data = openai.embeddings.create(input=input, model='text-embedding-ada-002').data
    return [i.embedding for i in data]


def create_avg_embeddings(input: str):
    chunks = string_into_chunks(input, 2048)
    embeddings = create_embeddings(chunks)
    return np.mean(np.array(embeddings), axis=0).tolist()


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


def search(query: str,  table_name: str, select='*', min_similarity=0, limit=10):
    query_embedding = create_embeddings(query)[0]

    with db_connection.cursor() as cursor:
        cursor.execute(f'''
          SELECT {select}, DOT_PRODUCT(JSON_ARRAY_PACK(%s), embedding) as similarity
          FROM {table_name}
          WHERE similarity > {min_similarity}
          ORDER BY similarity DESC
          LIMIT %s
        ''', [str(query_embedding), limit])

        return cursor.fetchall()
