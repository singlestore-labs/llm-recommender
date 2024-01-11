import os
from dotenv import load_dotenv

load_dotenv()

MODELS_LIMIT = 100

DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')
DB_NAME = os.environ.get('DB_NAME')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

HF_TOKEN = os.getenv('HF_TOKEN')

TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

LEADERBOARD_DATASET_URL = 'https://llm-recommender.vercel.app/datasets/leaderboard.json'

REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

TOKENS_LIMIT = 2047
TOKENS_TRASHHOLD_LIMIT = TOKENS_LIMIT - 128

MODELS_TABLE_NAME = 'models'
MODEL_READMES_TABLE_NAME = 'model_readmes'
MODEL_TWITTER_POSTS_TABLE_NAME = 'model_twitter_posts'
MODEL_REDDIT_POSTS_TABLE_NAME = 'model_reddit_posts'
MODEL_GITHUB_REPOS_TABLE_NAME = 'model_github_repos'
