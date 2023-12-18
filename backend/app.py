import os
import requests
from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')


def get_hf_model_downloads(repo_id: str):
    request_url = f'https://huggingface.co/api/models/{repo_id}'
    response = requests.get(request_url, headers={'Authorization': f'Bearer {HF_TOKEN}'})

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        return None


def get_hf_model_readme(repo_id: str):
    request_url = f'https://huggingface.co/{repo_id}/raw/main/README.md'
    response = requests.get(request_url)

    if response.status_code == 200:
        return response.text
    else:
        return ''


# get_hf_model_downloads('rwitz2/go-bruins-v2.1.1')
