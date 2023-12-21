import openai
import singlestoredb as s2

from src.constants import DB_CONNECTION_URL, OPENAI_API_KEY
from src.utils import create_embeddings

db_connection = s2.connect(DB_CONNECTION_URL)
openai.api_key = OPENAI_API_KEY


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
