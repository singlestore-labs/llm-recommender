import singlestoredb as s2

from src.constants import DB_CONNECTION_URL, DB_NAME

connection = s2.connect(DB_CONNECTION_URL)


def drop_table(table_name: str):
    with connection.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {DB_NAME}.{table_name}')


def get_models(select='*', query='', as_dict=True):
    with connection.cursor() as cursor:
        _query = f'SELECT {select} FROM models'

        if query:
            _query += f' {query}'

        cursor.execute(_query)

        if as_dict:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        return cursor.fetchall()
