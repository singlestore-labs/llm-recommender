import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')
DB_NAME = os.environ.get('DB_NAME')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

HF_TOKEN = os.getenv('HF_TOKEN')

TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
