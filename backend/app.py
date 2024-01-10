import src.db as db
import src.leaderboard as leaderboard
import src.twitter as twitter
import src.reddit as reddit
import src.github as github

db.drop_table('models')
db.drop_table('model_readmes')
db.drop_table('model_twitter_posts')
db.drop_table('model_reddit_posts')
db.drop_table('model_github_repos')

db.create_tables()

leaderboard.insert_models(leaderboard.get_models())

existed_models = db.get_models('repo_id, name', 'ORDER BY score DESC')

reddit.insert_models_posts(reddit.get_models_posts(existed_models))
twitter.insert_models_posts(twitter.get_models_posts(existed_models))
github.insert_models_repos(github.get_models_repos(existed_models))
