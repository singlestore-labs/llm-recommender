import praw

from .constants import REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

# https://www.reddit.com/prefs/apps
reddit = praw.Reddit(
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


def search_posts(keyword: str):
    posts = []

    # https://www.reddit.com/dev/api/#GET_search
    # https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.search
    for post in reddit.subreddit('all').search(keyword, sort='relevance'):
        if post.selftext and not post.over_18:
            posts.append({
                'id': post.id,
                'title': post.title,
                'text': post.selftext,
                'link': post.url,
                'created_at': post.created_utc,
            })

    return posts


def get_models_posts(models):
    models_posts = {}

    for model in models:
        repo_id = model['repo_id']
        keyword = repo_id
        posts = search_posts(keyword)
        models_posts[repo_id] = posts

    return models_posts
