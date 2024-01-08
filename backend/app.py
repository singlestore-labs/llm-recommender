import src.db as db
import src.leaderboard as leaderboard
import src.reddit as reddit
import src.github as github

db.drop_table('models')
db.drop_table('model_readmes')
db.drop_table('model_twitter_posts')
db.drop_table('model_reddit_posts')
db.drop_table('model_github_repos')

# db.create_tables()

# leaderboard_models = leaderboard.get_models()
# leaderboard.insert_models(leaderboard_models)

# existed_models = db.get_models('repo_id, name', 'ORDER BY score DESC')

# models_reddit_posts = reddit.get_models_posts(existed_models)
# reddit.insert_models_posts(models_reddit_posts)

# models_github_repos = github.get_models_repos(existed_models)
# github.insert_models_repos(models_github_repos)
