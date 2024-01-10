import re
import json
from datetime import datetime

from github import Github
from github import Auth

from . import constants
from . import db
from . import ai
from . import utils

github = Github(auth=Auth.Token(constants.GITHUB_ACCESS_TOKEN))


def search_repos(keyword: str, last_created_at):
    repos = []
    query = f'"{keyword}" in:name,description,readme'

    if last_created_at:
        query += f' created:>{last_created_at}'

    try:
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
    except Exception:
        return repos

    return repos


def get_models_repos(existed_models):
    repos = {}

    for model in existed_models:
        try:
            repo_id = model['repo_id']

            with db.connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT UNIX_TIMESTAMP(created_at) FROM {constants.MODEL_GITHUB_REPOS_TABLE_NAME}
                    WHERE model_repo_id = '{repo_id}'
                    ORDER BY created_at DESC
                    LIMIT 1
                """)

                last_created_at = cursor.fetchone()
                if (last_created_at):
                    last_created_at = datetime.fromtimestamp(float(last_created_at[0]))
                    last_created_at = last_created_at.strftime('%Y-%m-%dT%H:%M:%SZ')

            keyword = model['name'] if re.search(r'\d', model['name']) else repo_id
            found_repos = search_repos(keyword, last_created_at)

            if not len(found_repos):
                continue

            repos[repo_id] = found_repos
        except Exception as e:
            print(e)
            continue

    return repos


def insert_models_repos(repos):
    for model_repo_id, repos in repos.items():
        if not len(repos):
            continue

        for repo in repos:
            try:
                values = []
                value = {
                    'model_repo_id': model_repo_id,
                    'repo_id': repo['repo_id'],
                    'name': repo['name'],
                    'description': repo['description'],
                    'clean_text': utils.clean_string(repo['readme']),
                    'link': repo['link'],
                    'created_at': repo['created_at'],
                }

                to_embedding = {
                    'model_repo_id': model_repo_id,
                    'name': value['name'],
                    'description': value['description'],
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
                                INSERT INTO {constants.MODEL_GITHUB_REPOS_TABLE_NAME} (model_repo_id, repo_id, name, description, clean_text, link, created_at, embedding)
                                VALUES (%s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), JSON_ARRAY_PACK(%s))
                            ''', chunk)
            except Exception as e:
                print(e)
                continue
