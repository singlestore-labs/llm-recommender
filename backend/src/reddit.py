import re
import json
import praw

from .constants import REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from .db import db_connection
from .utils import create_avg_embeddings

# https://www.reddit.com/prefs/apps
reddit = praw.Reddit(
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


def search_posts(keyword: str, latest_post_timestamp):
    posts = []

    # https://www.reddit.com/dev/api/#GET_search
    # https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.search
    for post in reddit.subreddit('all').search(
            f'"{keyword}"', sort='relevance', time_filter='year', limit=100
    ):
        contains_keyword = keyword in post.title or keyword in post.selftext

        if contains_keyword and not post.over_18 and len(post.selftext) <= 7000:
            if not latest_post_timestamp or (post.created_utc > latest_post_timestamp):
                posts.append({
                    'post_id': post.id,
                    'title': post.title,
                    'text': post.selftext,
                    'link': f'https://www.reddit.com{post.permalink}',
                    'created_at': post.created_utc,
                })

    return posts


def get_models_posts(models):
    models_posts = {}

    for model in models:
        repo_id = model['repo_id']

        with db_connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT UNIX_TIMESTAMP(created_at) FROM models_reddit_posts
                WHERE model_repo_id = '{repo_id}'
                ORDER BY created_at DESC
                LIMIT 1
            """)

            latest_post_timestamp = cursor.fetchone()
            latest_post_timestamp = float(latest_post_timestamp[0]) if latest_post_timestamp != None else None

        keyword = model['name'] if re.search(r'\d', model['name']) else repo_id
        posts = search_posts(keyword, latest_post_timestamp)
        models_posts[repo_id] = posts

    return models_posts


def insert_models_posts(posts):
    with db_connection.cursor() as cursor:
        for model_repo_id, posts in posts.items():
            if not len(posts):
                continue

            cursor.executemany(
                f'''
                INSERT INTO models_reddit_posts (model_repo_id, post_id, title, text, link, created_at, embedding)
                VALUES (%s, %s, %s, %s, %s, FROM_UNIXTIME(%s), JSON_ARRAY_PACK(%s))
            ''',
                [(model_repo_id, post['post_id'],
                  post['title'],
                  post['text'],
                  post['link'],
                  post['created_at'],
                  str(create_avg_embeddings(json.dumps(post)))) for post in posts])
