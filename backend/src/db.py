import singlestoredb as s2
from datetime import datetime

from . import constants

connection = s2.connect(constants.DB_CONNECTION_URL)


def create_tables():
    def create_models_table():
        with connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {constants.MODELS_TABLE_NAME} (
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
        with connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {constants.MODEL_READMES_TABLE_NAME} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    clean_text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    created_at TIMESTAMP,
                    embedding BLOB
                )
            ''')

    def create_model_twitter_posts_table():
        with connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {constants.MODEL_TWITTER_POSTS_TABLE_NAME} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    post_id VARCHAR(256),
                    clean_text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    created_at TIMESTAMP,
                    embedding BLOB
                )
            ''')

    def create_model_reddit_posts_table():
        with connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {constants.MODEL_REDDIT_POSTS_TABLE_NAME} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    post_id VARCHAR(256),
                    title VARCHAR(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    clean_text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    link VARCHAR(256),
                    created_at TIMESTAMP,
                    embedding BLOB
                )
            ''')

    def create_model_github_repos_table():
        with connection.cursor() as cursor:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {constants.MODEL_GITHUB_REPOS_TABLE_NAME} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_repo_id VARCHAR(512),
                    repo_id INT,
                    name VARCHAR(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
                    clean_text LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
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


def drop_table(table_name: str):
    with connection.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {constants.DB_NAME}.{table_name}')


def get_models(select='*', query='', as_dict=True):
    with connection.cursor() as cursor:
        _query = f'SELECT {select} FROM {constants.MODELS_TABLE_NAME}'

        if query:
            _query += f' {query}'

        cursor.execute(_query)

        if as_dict:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        return cursor.fetchall()


def db_get_last_created_at(table, repo_id, to_string=False):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT UNIX_TIMESTAMP(created_at) FROM {table}
            WHERE model_repo_id = '{repo_id}'
            ORDER BY created_at DESC
            LIMIT 1
        """)

        rows = cursor.fetchone()
        created_at = float(rows[0]) if rows and rows[0] else None

        if (created_at and to_string):
            created_at = datetime.fromtimestamp(created_at)
            created_at = created_at.strftime('%Y-%m-%dT%H:%M:%SZ')

        return created_at
