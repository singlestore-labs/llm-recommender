from importlib.resources import read_text
import re
import json
import requests
from datetime import datetime
from time import time, sleep

from . import constants
from . import db
from . import ai
from . import utils


def github_search_repos(keyword: str, last_created_at):
    repos = []
    headers = {'Authorization': f'token {constants.GITHUB_ACCESS_TOKEN}'}
    query = f'"{keyword}" in:name,description,readme'

    if last_created_at:
        query += f' created:>{last_created_at}'

    try:
        repos_response = requests.get(
            "https://api.github.com/search/repositories",
            headers=headers,
            params={'q': query}
        )

        if repos_response.status_code == 403:
            # Handle rate limiting
            rate_limit = repos_response.headers['X-RateLimit-Reset']
            if not rate_limit:
                return repos

            sleep_time = int(rate_limit) - int(time())
            if sleep_time > 0:
                print(f"Rate limit exceeded. Retrying in {sleep_time} seconds.")
            sleep(sleep_time)
            return github_search_repos(keyword, last_created_at)

        if repos_response.status_code != 200:
            return repos

        for repo in repos_response.json().get('items', []):
            try:
                readme_response = requests.get(repo['contents_url'].replace('{+path}', 'README.md'), headers=headers)
                if repos_response.status_code != 200:
                    continue

                readme_file = readme_response.json()
                if readme_file['size'] > 7000:
                    continue

                readme_text = requests.get(readme_file['download_url']).text
                if not readme_text:
                    continue

                repos.append({
                    'repo_id': repo['id'],
                    'name': repo['name'],
                    'link': repo['html_url'],
                    'created_at': datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp(),
                    'description': repo.get('description', ''),
                    'readme': readme_text,
                })
            except:
                continue
    except:
        return repos

    return repos


def github_insert_model_repos(model_repo_id, repos):
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
            print('Error github_insert_model_repos: ', e)


def github_process_models_repos(existed_models):
    print('Processing GitHub posts')

    for model in existed_models:
        try:
            repo_id = model['repo_id']
            last_created_at = db.db_get_last_created_at(constants.MODEL_GITHUB_REPOS_TABLE_NAME, repo_id, True)
            keyword = model['name'] if re.search(r'\d', model['name']) else repo_id
            found_repos = github_search_repos(keyword, last_created_at)

            if len(found_repos):
                github_insert_model_repos(repo_id, found_repos)
        except Exception as e:
            print('Error github_process_models_repos: ', e)
