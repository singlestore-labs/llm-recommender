import re
import json
import datetime

from github import Github
from github import Auth

from .constants import GITHUB_ACCESS_TOKEN
from .db import db_connection
from .utils import create_avg_embeddings

github = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))


def search_repos(keyword: str, last_repo_created_at):
    repos = []
    query = f'"{keyword}" in:name,description,readme'

    if last_repo_created_at:
        query += f' created>:{last_repo_created_at}'

    for repo in github.search_repositories(query):
        try:
            readme_file = repo.get_readme()

            if readme_file.size > 7000:
                continue

            readme = readme_file.decoded_content.decode('utf-8')

            repos.append({
                'repo_id': repo.id,
                'name': repo.name,
                'link': repo.html_url,
                'created_at': repo.created_at.timestamp(),
                'description': repo.description if bool(repo.description) else '',
                'readme': readme,
            })
        except:
            continue

    return repos


def get_models_repos(models):
    models_repos = {}

    for model in models:
        try:
            repo_id = model['repo_id']

            with db_connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT UNIX_TIMESTAMP(created_at) FROM models_github_repos
                    WHERE model_repo_id = '{repo_id}'
                    ORDER BY created_at DESC
                    LIMIT 1
                """)

                last_repo_crated_at = cursor.fetchone()
                if (last_repo_crated_at):
                    last_repo_crated_at = datetime.datetime.fromtimestamp(float(last_repo_crated_at[0]))
                    last_repo_crated_at = last_repo_crated_at.strftime("%Y-%m-%d")

            keyword = model['name'] if re.search(r'\d', model['name']) else repo_id
            repos = search_repos(keyword, last_repo_crated_at)
            models_repos[repo_id] = repos
        except:
            models_repos[repo_id] = []

    return models_repos


def insert_models_repos(repos):
    with db_connection.cursor() as cursor:
        for model_repo_id, repos in repos.items():
            if not len(repos):
                continue

            cursor.executemany(
                f'''
                INSERT INTO models_github_repos (model_repo_id, repo_id, name, description, readme, link, created_at, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), JSON_ARRAY_PACK(%s))
            ''',
                [(model_repo_id, repo['repo_id'],
                  repo['name'],
                  repo['description'],
                  repo['readme'],
                  repo['link'],
                  repo['created_at'],
                  str(create_avg_embeddings(json.dumps(repo)))) for repo in repos])
