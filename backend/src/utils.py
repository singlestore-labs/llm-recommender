import re
import json
from bs4 import BeautifulSoup
from markdown import markdown
from datetime import datetime

from .constants import TOKENS_LIMIT
from . import ai


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)


def string_into_chunks(string: str, max_tokens=TOKENS_LIMIT):
    if ai.count_tokens(string) <= max_tokens:
        return [string]

    delimiter = ' '
    words = string.split(delimiter)
    chunks = []
    current_chunk = []

    for word in words:
        if ai.count_tokens(delimiter.join(current_chunk + [word])) <= max_tokens:
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
    new_string = re.sub(r'====+', '=', new_string)
    new_string = remove_links(new_string)

    return new_string
