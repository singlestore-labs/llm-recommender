import json
import openai
import re
import tiktoken
from bs4 import BeautifulSoup
from datetime import datetime
from decimal import Decimal
from markdown import markdown


from .constants import DB_NAME, OPENAI_API_KEY, TOKENS_LIMIT
from .db import db_connection

openai.api_key = OPENAI_API_KEY


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def count_tokens(text: str):
    enc = tiktoken.get_encoding('cl100k_base')
    return len(enc.encode(text))


def string_into_chunks(string: str, max_tokens=TOKENS_LIMIT):
    if count_tokens(string) <= max_tokens:
        return [string]

    delimiter = ' '
    words = string.split(delimiter)
    chunks = []
    current_chunk = []

    for word in words:
        if count_tokens(delimiter.join(current_chunk + [word])) <= max_tokens:
            current_chunk.append(word)
        else:
            chunks.append(delimiter.join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(delimiter.join(current_chunk))

    return chunks


def clean_string(string: str):
    def strip_html_elements(string: str):
        html = markdown(string)
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        return text.strip()

    def remove_unicode_escapes(string: str):
        return re.sub(r'[^\x00-\x7F]+', '', string)

    def remove_string_spaces(strgin: str):
        new_string = re.sub(r'\n+', '\n', strgin)
        new_string = re.sub(r'\s+', ' ', new_string)
        return new_string

    def remove_links(string: str):
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', string)

    new_string = strip_html_elements(string)
    new_string = remove_unicode_escapes(new_string)
    new_string = remove_string_spaces(new_string)
    new_string = re.sub(r'\*\*+', '*', new_string)
    new_string = re.sub(r'--+', '-', new_string)
    new_string = remove_links(new_string)
    return new_string


def create_embeddings(input):
    data = openai.embeddings.create(input=input, model='text-embedding-ada-002').data
    return [i.embedding for i in data]


def get_models(select='*', query='', as_dict=True):
    with db_connection.cursor() as cursor:
        _query = f'SELECT {select} FROM models'

        if query:
            _query += f' {query}'

        cursor.execute(_query)

        if as_dict:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        return cursor.fetchall()


def drop_table(table_name: str):
    with db_connection.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {DB_NAME}.{table_name}')
