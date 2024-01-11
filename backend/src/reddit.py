import re
import json
import praw

from . import constants
from . import db
from . import ai
from . import utils

# https://www.reddit.com/prefs/apps
reddit = praw.Reddit(
    username=constants.REDDIT_USERNAME,
    password=constants.REDDIT_PASSWORD,
    client_id=constants.REDDIT_CLIENT_ID,
    client_secret=constants.REDDIT_CLIENT_SECRET,
    user_agent=constants.REDDIT_USER_AGENT
)


def reddit_search_posts(keyword: str, last_created_at):
    posts = []

    # https://www.reddit.com/dev/api/#GET_search
    # https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.search
    try:
        for post in reddit.subreddit('all').search(
            f'"{keyword}"', sort='relevance', time_filter='year', limit=100
        ):
            contains_keyword = keyword in post.title or keyword in post.selftext

            if contains_keyword and not post.over_18:
                if not last_created_at or (post.created_utc > last_created_at):
                    posts.append({
                        'post_id': post.id,
                        'title': post.title,
                        'text': post.selftext,
                        'link': f'https://www.reddit.com{post.permalink}',
                        'created_at': post.created_utc,
                    })
    except Exception as e:
        print('Error reddit_search_posts: ', e)
        return posts

    return posts


def reddit_insert_model_posts(model_repo_id, posts):
    for post in posts:
        try:
            values = []

            value = {
                'model_repo_id': model_repo_id,
                'post_id': post['post_id'],
                'title': post['title'],
                'clean_text': utils.clean_string(post['text']),
                'link': post['link'],
                'created_at': post['created_at'],
            }

            to_embedding = {
                'model_repo_id': model_repo_id,
                'title': value['title'],
                'clean_text': value['clean_text']
            }

            if ai.count_tokens(value['clean_text']) <= constants.TOKENS_TRASHHOLD_LIMIT:
                embedding = str(ai.create_embedding(json.dumps(to_embedding)))
                values.append({**value, 'embedding': embedding})
            else:
                for chunk in utils.string_into_chunks(value['clean_text']):
                    embedding = str(ai.create_embedding(json.dumps({
                        **to_embedding,
                        'clean_text': chunk
                    })))
                    values.append({**value, 'clean_text': chunk, 'embedding': embedding})

            for chunk in utils.list_into_chunks([list(value.values()) for value in values]):
                with db.connection.cursor() as cursor:
                    cursor.executemany(f'''
                        INSERT INTO {constants.MODEL_REDDIT_POSTS_TABLE_NAME} (model_repo_id, post_id, title, clean_text, link, created_at, embedding)
                        VALUES (%s, %s, %s, %s, %s, FROM_UNIXTIME(%s), JSON_ARRAY_PACK(%s))
                    ''', chunk)
        except Exception as e:
            print('Error reddit_insert_model_posts: ', e)


def reddit_process_models_posts(existed_models):
    print('Processing Reddit posts')

    for model in existed_models:
        try:
            repo_id = model['repo_id']
            last_created_at = db.db_get_last_created_at(constants.MODEL_REDDIT_POSTS_TABLE_NAME, repo_id)
            keyword = model['name'] if re.search(r'\d', model['name']) else repo_id
            found_posts = reddit_search_posts(keyword, last_created_at)

            if len(found_posts):
                reddit_insert_model_posts(repo_id, found_posts)
        except Exception as e:
            print('Error reddit_process_models_posts: ', e)
