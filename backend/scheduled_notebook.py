import openai

from src.constants import OPENAI_API_KEY
import src.db as db
import src.leaderboard as leaderboard
import src.reddit as reddit
import src.github as github

openai.api_key = OPENAI_API_KEY

leaderbard_models = leaderboard.get_models()
leaderboard.insert_models(leaderbard_models)

models = db.get_models('name, author, repo_id', 'ORDER BY score DESC')

models_reddit_posts = reddit.get_models_posts(models)
reddit.insert_models_posts(models_reddit_posts)

models_github_repos = github.get_models_repos(models)
github.insert_models_repos(models_github_repos)
