import json
import requests
import pandas as pd
from time import time

from . import constants
from . import db
from . import ai
from . import utils


def leaderboard_get_df():
    response = requests.get(constants.LEADERBOARD_DATASET_URL)

    if response.status_code == 200:
        data = json.loads(response.text)
        df = pd.DataFrame(data).head(constants.MODELS_LIMIT)
        return df
    else:
        print("Failed to retrieve JSON file")


def leaderboard_insert_model(model):
    try:
        _model = {key: value for key, value in model.items() if key != 'readme'}
        to_embedding = json.dumps(_model, cls=utils.JSONEncoder)
        embedding = str(ai.create_embedding(to_embedding))
        model_to_insert = {**_model, embedding: embedding}
        readmes_to_insert = []

        if model['readme']:
            readme = {
                'model_repo_id': model['repo_id'],
                'text': model['readme'],
                'created_at': time()
            }

            if ai.count_tokens(readme['text']) <= constants.TOKENS_TRASHHOLD_LIMIT:
                readme['clean_text'] = utils.clean_string(readme['text'])
                to_embedding = json.dumps({
                    'model_repo_id': readme['model_repo_id'],
                    'clean_text': readme['clean_text'],
                })
                readme['embedding'] = str(ai.create_embedding(to_embedding))
                readmes_to_insert.append(readme)
            else:
                for i, chunk in enumerate(utils.string_into_chunks(readme['text'])):
                    _readme = {
                        **readme,
                        'text': chunk,
                        'created_at': time()
                    }

                    _readme['clean_text'] = utils.clean_string(chunk)
                    to_embedding = json.dumps({
                        'model_repo_id': _readme['model_repo_id'],
                        'clean_text': chunk,
                    })
                    _readme['embedding'] = str(ai.create_embedding(to_embedding))
                    readmes_to_insert.append(_readme)

        with db.connection.cursor() as cursor:
            cursor.execute(f'''
                INSERT INTO {constants.MODELS_TABLE_NAME} (name, author, repo_id, score, link, still_on_hub, arc, hellaswag, mmlu, truthfulqa, winogrande, gsm8k, downloads, likes, created_at, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), JSON_ARRAY_PACK(%s))
            ''', tuple(model_to_insert.values()))

        for chunk in utils.list_into_chunks([tuple(readme.values()) for readme in readmes_to_insert]):
            with db.connection.cursor() as cursor:
                cursor.executemany(f'''
                    INSERT INTO {constants.MODEL_READMES_TABLE_NAME} (model_repo_id, text, created_at, clean_text, embedding)
                    VALUES (%s, %s, FROM_UNIXTIME(%s), %s, JSON_ARRAY_PACK(%s))
                ''', chunk)
    except Exception as e:
        print(e)


def leaderboard_process_models():
    existed_model_repo_ids = [i[0] for i in db.get_models('repo_id', as_dict=False)]
    leaderboard_df = leaderboard_get_df()

    for i, row in leaderboard_df.iterrows():
        if row['repo_id'] in existed_model_repo_ids:
            continue

        leaderboard_insert_model(row.to_dict())
