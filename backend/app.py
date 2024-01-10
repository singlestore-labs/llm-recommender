import src.db as db
from src.github import github_process_models_repos
from src.leaderboard import leaderboard_process_models
from src.reddit import reddit_process_models_posts
from src.twitter import twitter_process_models_posts

db.drop_table('models')
db.drop_table('model_readmes')
db.drop_table('model_twitter_posts')
db.drop_table('model_reddit_posts')
db.drop_table('model_github_repos')

db.create_tables()

print('Processing models')
leaderboard_process_models()

existed_models = db.get_models('repo_id, name', 'ORDER BY score DESC')

print('Processing Twitter posts')
twitter_process_models_posts(existed_models)

print('Processing Reddit posts')
reddit_process_models_posts(existed_models)

print('Processing GitHub posts')
github_process_models_repos(existed_models)
