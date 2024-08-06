import os
import base64
from aiohttp import ClientSession
from urllib.parse import urlparse
from setup import LANGUAGE_MAPPING


async def fetch(url: str, session: ClientSession, headers=None):
    async with session.get(url, headers=headers) as response:
        print("Request to ", url)
        return response.status, await response.text()


def get_repo_name(url: str):
    path_parts = urlparse(url).path.split("/")
    return f"{path_parts[2]}/{path_parts[3]}"


def check_file(path: str):
    filename, file_extension = os.path.splitext(path)
    if file_extension in LANGUAGE_MAPPING.values():
        return True
    return False


def decode(content: str):
    return base64.b64decode(content).decode("utf-8")
