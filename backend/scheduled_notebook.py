import openai

from src.constants import OPENAI_API_KEY
from src.db import db_connection
from src.utils import create_embeddings, get_models
import src.twitter as twitter
import src.reddit as reddit
import src.github as github

openai.api_key = OPENAI_API_KEY

models = get_models('name, author, repo_id', 'ORDER BY score DESC')[:50]


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


# models_tweets = twitter.get_models_tweets(models)
# print(models_tweets)

models_reddit_posts = reddit.get_models_posts(models)
reddit.insert_models_posts(models_reddit_posts)

models_github_repos = github.get_models_repos(models)
github.insert_models_repos(models_github_repos)
