import re

from github import Github
from github import Auth

from .constants import GITHUB_ACCESS_TOKEN

github = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))


def search_repos(keyword: str):
    repos = []

    for repo in github.search_repositories(f'"{keyword}" in:name,description,readme'):
        try:
            readme_file = repo.get_readme()

            if readme_file.size > 5000:
                continue

            readme = readme_file.decoded_content.decode('utf-8')

            repos.append({
                'id': repo.id,
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
            keyword = model['name'] if re.search(r'\d', model['name']) else repo_id
            repos = search_repos(keyword)
            models_repos[repo_id] = repos
        except:
            models_repos[repo_id] = []

    return models_repos
