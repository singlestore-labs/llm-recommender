import openai
import tiktoken

from . import constants

openai.api_key = constants.OPENAI_API_KEY


def count_tokens(text: str):
    enc = tiktoken.get_encoding('cl100k_base')
    return len(enc.encode(text, disallowed_special={}))


def create_embedding(input):
    data = openai.embeddings.create(input=input, model='text-embedding-ada-002').data
    return data[0].embedding
