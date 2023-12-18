import requests


def get_hf_model_downloads(model_full_name):
    return 0


def get_hf_model_readme(model_full_name):
    readme_url = f"https://huggingface.co/{model_full_name}/raw/main/README.md"
    response = requests.get(readme_url)

    if response.status_code == 200:
        return response.text
    else:
        return ''
